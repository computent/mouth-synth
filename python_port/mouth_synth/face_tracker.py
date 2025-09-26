"""MediaPipe FaceMesh wrapper matching the JavaScript ml5 manager."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Optional

import mediapipe as mp
import numpy as np

from .config import Ml5Config


@dataclass
class FaceMetrics:
    lips_opening: float
    lips_rotation: float
    tip_heading_x: float
    tip_heading_y: float


class FaceTracker:
    def __init__(self, config: Ml5Config) -> None:
        self.config = config
        self.mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self._lips_open_samples: Deque[float] = deque(maxlen=5)
        self._rotation_samples: Deque[float] = deque(maxlen=5)

    def process(self, frame: np.ndarray) -> Optional[FaceMetrics]:
        frame.flags.writeable = False
        results = self.mesh.process(frame)
        frame.flags.writeable = True
        if not results.multi_face_landmarks:
            return None

        face_landmarks = results.multi_face_landmarks[0]
        points = np.array([(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark])

        opening = self._compute_lip_opening(points)
        rotation = self._compute_rotation(points)
        tip_heading = self._compute_tip_heading(points)

        self._lips_open_samples.append(opening)
        self._rotation_samples.append(rotation)

        return FaceMetrics(
            lips_opening=np.mean(self._lips_open_samples),
            lips_rotation=np.mean(self._rotation_samples),
            tip_heading_x=tip_heading[0],
            tip_heading_y=tip_heading[1],
        )

    def _compute_lip_opening(self, points: np.ndarray) -> float:
        top_lip = points[13]  # upper lip landmark
        bottom_lip = points[14]  # lower lip landmark
        distance = np.linalg.norm(top_lip - bottom_lip)
        return distance * 100  # scale for easier thresholds

    def _compute_rotation(self, points: np.ndarray) -> float:
        left_mouth = points[61]
        right_mouth = points[291]
        delta = right_mouth - left_mouth
        return np.degrees(np.arctan2(delta[1], delta[0]))

    def _compute_tip_heading(self, points: np.ndarray) -> np.ndarray:
        tip = points[0]
        nose = points[1]
        vector = tip - nose
        return vector[:2] * 100

    def close(self) -> None:
        self.mesh.close()


__all__ = ["FaceTracker", "FaceMetrics"]

"""Video capture and drawing utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import cv2
import numpy as np

from .config import VideoConfig


@dataclass
class FrameBundle:
    frame: np.ndarray
    surface: np.ndarray


class VideoManager:
    """Wraps OpenCV capture with simple pixelation and mirroring."""

    def __init__(self, config: VideoConfig) -> None:
        self.config = config
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            raise RuntimeError("Could not open default webcam (index 0).")

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)

    def read(self) -> FrameBundle:
        success, frame = self.capture.read()
        if not success:
            raise RuntimeError("Failed to read frame from webcam.")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if self.config.flipped:
            frame = cv2.flip(frame, 1)

        pixelated = self._pixelate(frame)
        overlay = self._apply_overlay(pixelated)
        return FrameBundle(frame=frame, surface=overlay)

    def _pixelate(self, frame: np.ndarray) -> np.ndarray:
        short_side = min(frame.shape[:2])
        downscale = max(1, short_side // self.config.pixelation_short_side_num)
        small = cv2.resize(frame, (frame.shape[1] // downscale, frame.shape[0] // downscale), interpolation=cv2.INTER_LINEAR)
        return cv2.resize(small, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)

    def _apply_overlay(self, frame: np.ndarray) -> np.ndarray:
        alpha = self.config.overlay_color[3] / 255.0
        overlay_color = np.array(self.config.overlay_color[:3], dtype=frame.dtype)
        blended = cv2.addWeighted(frame, 1 - alpha, overlay_color, alpha, 0)
        return blended

    def release(self) -> None:
        self.capture.release()


__all__ = ["VideoManager", "FrameBundle"]

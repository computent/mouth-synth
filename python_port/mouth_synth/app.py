"""Main application loop that mirrors the JavaScript sketch."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pygame

from .config import AppConfig
from .face_tracker import FaceMetrics, FaceTracker
from .sound import SoundManager
from .ui import UiManager
from .video import FrameBundle, VideoManager


@dataclass
class AppState:
    audio_started: bool = False
    face_metrics: Optional[FaceMetrics] = None
    face_detected: bool = False
    last_face_time: float = 0.0


class MouthSynthApp:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.video = VideoManager(config.video)
        self.face_tracker = FaceTracker(config.ml5)
        self.sound = SoundManager(config.sound)
        self.ui = UiManager(config.ui)
        pygame.init()
        self.screen = pygame.display.set_mode((config.video.width, config.video.height))
        pygame.display.set_caption("Mouth Synth (Python)")
        self.clock = pygame.time.Clock()
        self.state = AppState()

    def run(self) -> None:
        try:
            running = True
            while running:
                running = self._handle_events()
                bundle = self.video.read()
                metrics = self.face_tracker.process(bundle.frame)
                self._update_state(metrics)
                self._update_audio()
                self._draw(bundle)
                self.clock.tick(self.config.fps)
        finally:
            self._shutdown()

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state.audio_started = True
        return True

    def _update_state(self, metrics: Optional[FaceMetrics]) -> None:
        self.state.face_metrics = metrics
        self.state.face_detected = metrics is not None
        if metrics:
            self.state.last_face_time = time.time()
        self.ui.update(
            ready=True,
            audio_started=self.state.audio_started,
            face_detected=self.state.face_detected,
        )

    def _update_audio(self) -> None:
        metrics = self.state.face_metrics
        if not self.state.audio_started or metrics is None:
            self.sound.trigger_end()
            return

        opening = metrics.lips_opening
        opening_pct = np.clip(opening / (self.config.ml5.lips_open_threshold * 2), 0.0, 1.0)
        rotation_pct = np.clip((metrics.lips_rotation + 45) / 90, 0.0, 1.0)
        heading_x_pct = np.clip((metrics.tip_heading_x + 50) / 100, 0.0, 1.0)
        heading_y_pct = np.clip((metrics.tip_heading_y + 50) / 100, 0.0, 1.0)

        if opening > self.config.ml5.lips_open_threshold:
            self.sound.trigger_start(rotation_pct)
        elif opening < self.config.ml5.lips_close_threshold:
            self.sound.trigger_end()

        self.sound.change_volume(opening_pct)
        self.sound.detune(rotation_pct)
        self.sound.change_effect_frequency(rotation_pct)
        self.sound.move_harmonicity(heading_x_pct)
        self.sound.change_modulation_index(heading_y_pct)

    def _draw(self, bundle: FrameBundle) -> None:
        frame_surface = pygame.surfarray.make_surface(np.rot90(bundle.surface))
        self.screen.blit(frame_surface, (0, 0))
        self.ui.draw(self.screen)
        pygame.display.flip()

    def _shutdown(self) -> None:
        self.sound.close()
        self.face_tracker.close()
        self.video.release()
        pygame.quit()


__all__ = ["MouthSynthApp"]

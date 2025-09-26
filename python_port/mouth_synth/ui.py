"""UI rendering helpers for Pygame."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from .config import UiConfig


@dataclass
class UiState:
    message: str = ""
    loading: bool = True
    face_detected: bool = False


class UiManager:
    def __init__(self, config: UiConfig) -> None:
        self.config = config
        pygame.font.init()
        try:
            self.font = pygame.font.Font(self.config.font_path, 24)
        except FileNotFoundError:
            self.font = pygame.font.SysFont("Arial", 24)
        self.state = UiState(message=self.config.messages.loading)

    def update(self, ready: bool, audio_started: bool, face_detected: bool) -> None:
        if not ready:
            self.state = UiState(message=self.config.messages.loading, loading=True)
        elif not audio_started:
            self.state = UiState(message=self.config.messages.welcome, loading=False)
        elif not face_detected:
            self.state = UiState(message=self.config.messages.running or "NO FACE DETECTED", loading=False)
        else:
            self.state = UiState(message=self.config.messages.running, loading=False, face_detected=True)

    def draw(self, surface: pygame.Surface) -> None:
        if not self.state.message:
            return
        text_surface = self.font.render(self.state.message, True, self.config.text_color)
        rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() - 50))
        surface.blit(text_surface, rect)


__all__ = ["UiManager"]

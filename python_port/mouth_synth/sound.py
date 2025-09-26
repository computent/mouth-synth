"""Simplified Tone.js-inspired synthesiser built on Pygame."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pygame

from .config import SoundConfig


@dataclass
class SynthState:
    frequency: float
    modulation_index: float
    harmonicity: float
    volume: float


class SoundManager:
    def __init__(self, config: SoundConfig, sample_rate: int = 44100) -> None:
        self.config = config
        self.sample_rate = sample_rate
        self.current_state = SynthState(
            frequency=440.0,
            modulation_index=10.0,
            harmonicity=3.0,
            volume=0.5,
        )
        self.channel: Optional[pygame.mixer.Channel] = None
        pygame.mixer.pre_init(sample_rate=sample_rate, size=-16, channels=1)
        pygame.mixer.init()

    def trigger_start(self, rotation_pct: float) -> None:
        note_idx = self._quantise_rotation(rotation_pct)
        midi_note = self.config.midi_scale[self.config.note_indices[note_idx]]
        frequency = 440.0 * (2 ** ((midi_note - 69) / 12))
        self.current_state.frequency = frequency
        self._play_tone()

    def trigger_end(self) -> None:
        if self.channel:
            self.channel.fadeout(100)

    def change_volume(self, opening_pct: float) -> None:
        self.current_state.volume = max(0.05, min(1.0, opening_pct))
        if self.channel:
            self.channel.set_volume(self.current_state.volume)

    def detune(self, rotation_pct: float) -> None:
        detune_cents = (rotation_pct - 0.5) * self.config.detune_amount
        self.current_state.frequency *= 2 ** (detune_cents / 1200)
        self._play_tone()

    def change_effect_frequency(self, rotation_pct: float) -> None:
        self.current_state.modulation_index = 1 + rotation_pct * self.config.effect_frequency_amount
        self._play_tone()

    def move_harmonicity(self, heading_pct: float) -> None:
        self.current_state.harmonicity = 1 + heading_pct * self.config.harmonicity_amount
        self._play_tone()

    def change_modulation_index(self, heading_pct: float) -> None:
        self.current_state.modulation_index = 1 + heading_pct * self.config.modulation_amount
        self._play_tone()

    def _quantise_rotation(self, rotation_pct: float) -> int:
        idx = int(rotation_pct * len(self.config.note_indices))
        return max(0, min(len(self.config.note_indices) - 1, idx))

    def _play_tone(self) -> None:
        duration = 0.25
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        modulator = np.sin(2 * np.pi * self.current_state.frequency * self.current_state.harmonicity * t)
        carrier = np.sin(
            2 * np.pi * self.current_state.frequency * t +
            self.current_state.modulation_index * modulator
        )
        waveform = (carrier * self.current_state.volume).astype(np.float32)
        sound = pygame.sndarray.make_sound((waveform * 32767).astype(np.int16))
        if self.channel:
            self.channel.stop()
        self.channel = sound.play(-1)
        if self.channel:
            self.channel.set_volume(self.current_state.volume)

    def get_waveform_values(self, samples: int = 128) -> np.ndarray:
        t = np.linspace(0, 1, samples)
        return np.sin(2 * np.pi * t)

    def close(self) -> None:
        pygame.mixer.quit()


__all__ = ["SoundManager"]

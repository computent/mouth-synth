"""Configuration models that mirror the JavaScript options."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class ExhibitConfig:
    reload_total_ms: int = 3_600_000
    reload_absence_ms: int = 10_000


@dataclass
class SoundEffectConfig:
    frequency: float = 5.0
    depth: float = 1.0


@dataclass
class SoundConfig:
    midi_scale: List[int] = field(
        default_factory=lambda: list(range(60, 85))
    )
    note_indices: List[int] = field(
        default_factory=lambda: [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24]
    )
    detune_amount: float = 512.0
    effect_frequency_amount: float = 16.0
    harmonicity_amount: float = 16.0
    modulation_amount: float = 64.0
    volume_amount: float = 16.0
    effect: SoundEffectConfig = field(default_factory=SoundEffectConfig)


@dataclass
class Ml5Config:
    lips_close_threshold: float = 4.0
    lips_open_threshold: float = 8.0
    idle_volume_factor: float = 0.5
    smoothness: float = 0.75
    stroke_weight: float = 0.01
    stroke_color: Tuple[int, int, int] = (255, 255, 255)
    glowing_stroke_weight: float = 0.015
    glowing_stroke_color: Tuple[int, int, int] = (255, 255, 255)
    lips_size: float = 0.75
    placeholder_faces_path: str | None = "assets/demo-faces.json"
    blurriness: float = 0.0


@dataclass
class VideoConfig:
    width: int = 480
    height: int = 480
    pixelation_short_side_num: int = 24
    pixelation_style: int = 6
    flipped: bool = True
    background_color: Tuple[int, int, int] = (0, 0, 0)
    overlay_color: Tuple[int, int, int, int] = (0, 0, 0, 100)
    min_factor_size: float = 0.3
    max_factor_size: float = 0.9


@dataclass
class UiMessages:
    loading: str = "LOADING..."
    welcome: str = "CLICK HERE TO ACTIVATE AUDIO"
    running: str = ""


@dataclass
class UiConfig:
    font_path: str = "assets/Ubuntu-Bold.ttf"
    text_color: Tuple[int, int, int] = (255, 255, 255)
    messages: UiMessages = field(default_factory=UiMessages)


@dataclass
class AppConfig:
    fps: int = 60
    exhibit: ExhibitConfig = field(default_factory=ExhibitConfig)
    sound: SoundConfig = field(default_factory=SoundConfig)
    ml5: Ml5Config = field(default_factory=Ml5Config)
    video: VideoConfig = field(default_factory=VideoConfig)
    ui: UiConfig = field(default_factory=UiConfig)

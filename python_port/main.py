"""Convenience launcher for the Mouth Synth Python port."""

from mouth_synth import AppConfig, MouthSynthApp


if __name__ == "__main__":
    MouthSynthApp(AppConfig()).run()

"""Command line entry point for the Mouth Synth application."""

from .app import MouthSynthApp
from .config import AppConfig


def main() -> None:
    app = MouthSynthApp(AppConfig())
    app.run()


if __name__ == "__main__":
    main()

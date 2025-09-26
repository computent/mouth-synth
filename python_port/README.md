# Mouth Synth (Python Port)

This package recreates the browser-based "Mouth Synth" experience using Python tooling. It captures webcam input with OpenCV, analyses lip landmarks via MediaPipe, and drives a small FM synthesiser implemented with NumPy and Pygame.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
pip install --upgrade pip
pip install -e .
```

> **Note**: MediaPipe requires additional system dependencies on some platforms. Consult the [MediaPipe installation guide](https://developers.google.com/mediapipe/solutions/vision/face_landmarker/python) if you encounter build errors.

## Usage
```bash
python -m mouth_synth
```

The program will open a Pygame window, start webcam capture, and play a sustained tone whenever your lips are detected as open. Moving your mouth changes pitch, modulation index, and harmonicity—mirroring the JavaScript original.

## Configuration
Runtime parameters such as MIDI scale, smoothing factors, and UI colours live in `mouth_synth/config.py`. Override them by creating a Python file and importing the module to mutate the dataclasses prior to launching.

## Packaging
Running `python -m build` from this directory will produce wheel and sdist archives suitable for distribution. Because OpenCV and MediaPipe ship platform-specific wheels, no extra binary build steps are necessary.

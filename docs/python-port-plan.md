# Python Port Technical Plan

This section summarises the technologies required to reproduce the browser experience in Python, discusses complexity trade-offs, and introduces the packaged reference implementation included in this repository.

## Core Technologies Needed
- **OpenCV (cv2)** – Captures webcam frames and performs image manipulation before rendering.
- **MediaPipe** – Provides cross-platform FaceMesh landmark detection comparable to ml5.js.
- **NumPy** – Efficient numerical operations for geometry and smoothing.
- **Pygame** – Hosts the application window, handles drawing, keyboard/mouse events, and can drive the main loop.
- **PyGame.midi** or **PyGame.sndarray** – For real-time audio playback; in this sample we drive a simple synthesiser using generated waveforms.
- **SoundDevice (optional)** – A lower-latency audio backend if you want to bypass Pygame's mixer.

## Complexity Compared to the Browser Version
- **Manual Event Loop** – Python requires explicit control over frame timing and event polling (handled by the browser/p5.js previously).
- **Threading/Async** – MediaPipe and OpenCV operate synchronously; keeping UI responsive often means introducing worker threads or buffering.
- **Audio Stack Differences** – Tone.js exposes high-level synth constructs; recreating this means building or integrating a synthesis layer manually (the included implementation demonstrates a basic FM synth in Python for parity).
- **Packaging & Distribution** – Unlike the single HTML bundle, Python needs dependency management (via `pip`), platform-specific runtime libraries (e.g., `portaudio`), and possibly virtual environment setup instructions.

Despite these added responsibilities, the Python port keeps concepts parallel to the JavaScript architecture: managers for video, face landmarks, sound, and UI orchestration.

## Included Reference Package
The repository now includes a `python_port/` directory with an installable package named `mouth-synth`. It mirrors the JavaScript managers:

| JavaScript Module        | Python Counterpart                           |
|--------------------------|----------------------------------------------|
| `scripts/videomanager.js`| `mouth_synth/video.py`                        |
| `scripts/ml5manager.js`  | `mouth_synth/face_tracker.py`                |
| `scripts/soundmanager.js`| `mouth_synth/sound.py`                        |
| `scripts/uimanager.js`   | `mouth_synth/ui.py`                           |
| `scripts/sketch.js`      | `mouth_synth/app.py` (ties everything together)|

### Features
- A cohesive `MouthSynthApp` class replicates the lip-controlled synthesiser workflow.
- Configuration mirrors the JS options, loaded from `mouth_synth/config.py` for clarity.
- Entry-point script `python_port/main.py` runs the app once dependencies are installed.
- `pyproject.toml` enables packaging and dependency installation via `pip install .`.

### Getting Started
1. Install system requirements (Python 3.10+, pip, development headers for PortAudio on macOS/Linux).
2. From the `python_port/` directory run `pip install -e .` to install the package in editable mode.
3. Execute `python -m mouth_synth` or `python main.py` to launch the experience.

The Python port is more verbose because it recreates browser conveniences manually, but the provided structure keeps it approachable and ready for deployment.

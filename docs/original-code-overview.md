# Original JavaScript Project Overview

This document walks through the structure of the existing p5.js + ml5.js project and explains, at a high level, what each script is responsible for. The goal is to give you a commented, holistic view of the original implementation before considering a port to Python.

## Entry Point (`index.html`)
- Loads p5.js, Tone.js, and ml5.js libraries.
- Includes the custom helper scripts (`videomanager.js`, `ml5manager.js`, `uimanager.js`, `soundmanager.js`) before finally loading `sketch.js`.
- Creates a p5.js instance that executes the exported `sketch` function defined in `scripts/sketch.js`.

## `scripts/sketch.js`
- Configures runtime options for the exhibit, audio synthesis, face tracking, video capture, and UI.
- Bootstraps the helper managers and wires the lip-motion callbacks to audio synthesis changes.
- Implements the main p5.js lifecycle (`preload`, `setup`, `draw`, etc.) to update the video feed, draw face landmarks, and render on-canvas UI messaging.
- Implements exhibit-specific behaviour (auto-reload after prolonged absence).

## `scripts/videomanager.js`
- Creates a hidden `createCapture` element using p5.js to stream from the webcam.
- Applies pixelation and color overlay effects before rendering the video texture onto the canvas each frame.
- Handles responsive scaling, mirroring, and fit/cover logic.

## `scripts/ml5manager.js`
- Wraps the ml5.js FaceMesh API to detect and track facial landmarks.
- Smooths landmark motion, determines lip open/close state, and exposes helper functions for lip rotation/opening percentages.
- Exposes callbacks (`lipsOpened`, `lipsClosed`, `lipsMovedWhileOpen`) that `sketch.js` wires into Tone.js parameter changes.

## `scripts/soundmanager.js`
- Configures a Tone.js AMSynth with a Chorus effect and waveform analyser.
- Responds to lip-motion callbacks by starting/stopping notes, detuning, modulating, and adjusting volume.
- Handles user-gesture requirements for enabling audio in browsers (`mousePressed`).

## `scripts/uimanager.js`
- Loads fonts, renders status text, and (optionally) the frame-rate display.
- Provides helper functions to update copy based on loading state and whether a face is currently detected.

With these components combined, the browser experience captures webcam footage, detects lip movements with MediaPipe (via ml5.js), and modulates a synthesizer in real time.

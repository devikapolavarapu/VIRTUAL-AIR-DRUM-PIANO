🎵 Virtual Air Drum & Piano

A real-time gesture-controlled virtual musical instrument that allows users to play drums and piano in mid-air using only a webcam.
The project uses computer vision and hand-gesture recognition to detect fingertip movements and trigger corresponding sounds with low latency.

This system demonstrates how Human–Computer Interaction (HCI) can be built using vision-based input instead of physical hardware.

🚀 Project Overview

Virtual Air Drum & Piano tracks hand landmarks in real time using MediaPipe, processes fingertip motion using OpenCV, and triggers instrument sounds using pygame.

The same gesture-detection pipeline supports two instrument modes:

🥁 Drum Mode – Percussion-based virtual drum pads

🎹 Piano Mode – Musical note-based virtual piano keys

The project is modular, scalable, and designed with extensibility in mind.

✨ Key Features

🎥 Live webcam-based hand tracking

✋ Fingertip detection using MediaPipe (21 landmarks)

⚡ Velocity-based downward tap detection (noise-resistant)

🧭 Spatial zone mapping for gesture interpretation

🔊 Low-latency real-time audio playback

🎹 Dual instrument support (Drum & Piano modes)

🧠 Clean cooldown & debouncing logic

⌨️ Press q to exit safely

🥁 Drum Mode

Drum Mode maps the screen into five vertical percussion zones:

Zone	Instrument
1	Kick
2	Snare
3	Hi-Hat
4	Tom
5	Clap

How it works:

A fast downward fingertip tap is detected

The X-axis position determines the drum zone

The corresponding drum sound is triggered

Run:

python main.py

🎹 Piano Mode

Piano Mode extends the same gesture pipeline to a melodic instrument.

The screen is divided into seven piano keys:

C   D   E   F   G   A   B


Each key corresponds to a musical note frequency.
A fingertip tap on a key triggers the respective note.

This mode demonstrates project extensibility without rewriting core logic.

Run:

python piano_mode.py

🛠️ Tech Stack
Category	Technologies
Programming Language	Python 3.10+
Computer Vision	OpenCV
Hand Tracking	MediaPipe
Audio Engine	pygame
Numerical Computing	NumPy
Version Control	Git & GitHub
🧩 System Architecture (High-Level)

Webcam captures live video frames

MediaPipe extracts hand landmarks

Fingertip coordinates are tracked per frame

Downward velocity is calculated to detect taps

X-axis position maps gesture to an instrument zone

Corresponding sound is played in real time

▶️ How to Run the Project
🔹 Prerequisites

Python 3.10 or higher

Functional webcam

Windows / macOS / Linux

🔹 Install Dependencies
pip install opencv-python mediapipe pygame numpy

🔹 Run Drum Mode
python main.py

🔹 Run Piano Mode
python piano_mode.py

🎮 How to Use

Place your hand in front of the webcam

Use your index finger

Perform a fast downward tap

Move left ↔ right to select instruments or notes

👩‍💻 Author

Devika Polavarapu
B.Tech – Information Technology

Interests:

Computer Vision

AI & Human–Computer Interaction

Real-world software systems

🔗 GitHub: https://github.com/devikapolavarapu

Press q to exit

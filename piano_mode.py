import os
os.environ["SDL_AUDIODRIVER"] = "directsound"

import cv2
import mediapipe as mp
import time
import pygame
import numpy as np

# ---------- INIT SOUND ----------
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(8)

def make_note(freq):
    sample_rate = 44100
    duration = 0.25

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)

    audio = np.int16(wave * 32767)
    stereo = np.column_stack((audio, audio))

    sound = pygame.sndarray.make_sound(stereo)
    sound.set_volume(1.0)
    return sound

# ---------- PIANO NOTES ----------
NOTES = {
    "C": make_note(261),
    "D": make_note(293),
    "E": make_note(329),
    "F": make_note(349),
    "G": make_note(392),
    "A": make_note(440),
    "B": make_note(493)
}

NOTE_NAMES = list(NOTES.keys())

# ---------- MediaPipe ----------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

# ---------- Camera ----------
cap = cv2.VideoCapture(0)

# ---------- Tap Detection ----------
prev_y = None
last_tap_time = 0
PIXEL_TAP_THRESHOLD = 25
COOLDOWN = 0.35

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # ---------- Draw Piano Keys ----------
    key_width = w // len(NOTE_NAMES)
    keys = []

    for i, name in enumerate(NOTE_NAMES):
        x1 = i * key_width
        x2 = x1 + key_width
        keys.append((x1, x2, name))

        cv2.rectangle(frame, (x1, 0), (x2, h), (200, 200, 200), 2)
        cv2.putText(
            frame,
            name,
            (x1 + 25, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2
        )

    # ---------- Hand Tracking ----------
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark[8]  # index finger tip

        cx = int(lm.x * w)
        cy = int(lm.y * h)

        cv2.circle(frame, (cx, cy), 12, (0, 255, 0), -1)

        if prev_y is not None:
            delta = cy - prev_y
            now = time.time()

            if delta > PIXEL_TAP_THRESHOLD and (now - last_tap_time) > COOLDOWN:
                last_tap_time = now

                for x1, x2, note in keys:
                    if x1 <= cx < x2:
                        NOTES[note].play()

                        cv2.putText(
                            frame,
                            f"NOTE: {note}",
                            (cx - 80, cy - 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.2,
                            (0, 0, 255),
                            4
                        )
                        break

        prev_y = cy

    cv2.imshow("Virtual Air Piano", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()


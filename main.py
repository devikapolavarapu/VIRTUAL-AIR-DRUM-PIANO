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

def make_sound(freq):
    sample_rate = 44100
    duration = 0.15

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)

    audio = np.int16(wave * 32767)
    stereo_audio = np.column_stack((audio, audio))

    sound = pygame.sndarray.make_sound(stereo_audio)
    sound.set_volume(1.0)  # force volume
    return sound

SOUNDS = {
    "Kick": make_sound(180),
    "Snare": make_sound(260),
    "HiHat": make_sound(400),
    "Tom": make_sound(320),
    "Clap": make_sound(520)
}

# ---------- MediaPipe ----------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

# ---------- Camera ----------
cap = cv2.VideoCapture(0)

# ---------- Tap detection ----------
prev_y = None
last_tap_time = 0
PIXEL_TAP_THRESHOLD = 25
COOLDOWN = 0.4

# ---------- Zones ----------
ZONE_NAMES = ["Kick", "Snare", "HiHat", "Tom", "Clap"]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    zone_width = w // 5
    zones = []
    for i, name in enumerate(ZONE_NAMES):
        x1 = i * zone_width
        x2 = x1 + zone_width
        zones.append((x1, x2, name))
        cv2.rectangle(frame, (x1, 0), (x2, h), (60, 60, 60), 2)
        cv2.putText(frame, name, (x1 + 20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (220, 220, 220), 2)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark[8]

        cx = int(lm.x * w)
        cy = int(lm.y * h)

        cv2.circle(frame, (cx, cy), 12, (0, 255, 0), -1)

        if prev_y is not None:
            delta = cy - prev_y
            now = time.time()

            if delta > PIXEL_TAP_THRESHOLD and (now - last_tap_time) > COOLDOWN:
                last_tap_time = now
                for x1, x2, name in zones:
                    if x1 <= cx < x2:
                        SOUNDS[name].play()
                        cv2.putText(frame, name, (cx - 60, cy - 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)
                        break

        prev_y = cy

    cv2.imshow("Virtual Air Drum", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()

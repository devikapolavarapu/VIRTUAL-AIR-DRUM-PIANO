import pygame
import numpy as np
import time

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

def beep():
    sample_rate = 44100
    duration = 0.5
    freq = 440

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(2 * np.pi * freq * t)
    audio = np.int16(wave * 32767)

    stereo = np.column_stack((audio, audio))
    sound = pygame.sndarray.make_sound(stereo)

    sound.set_volume(1.0)   # 🔥 FORCE MAX VOLUME
    sound.play()

print("Playing sound...")
beep()
time.sleep(1)
print("Done")

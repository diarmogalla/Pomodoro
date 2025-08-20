# sounds.py
import os

_mixer_ok = False
try:
    import pygame
    from pygame import mixer
    pygame.init()
    mixer.init()
    _mixer_ok = True
except Exception:
    _mixer_ok = False

def play_sound(path: str):
    if _mixer_ok and os.path.exists(path):
        try:
            mixer.music.load(path)
            mixer.music.play()
        except Exception:
            pass  # fail silently

def chime_default():
    # no-op if pygame not available; UI can also call root.bell() for a UI beep
    pass

import tempfile
import wave

import pygame


def play_audio(audio_segment):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
        audio_segment.export(f.name, format="wav")
        sound = pygame.mixer.Sound(f.name)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(100)


def get_wav_duration_seconds(filename: str) -> float:
    with wave.open(filename, "rb") as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    return duration


def calculate_bpm(filename: str, beats_per_loop: int = 4) -> float:
    duration = get_wav_duration_seconds(filename)
    bpm = (beats_per_loop / duration) * 60
    return bpm

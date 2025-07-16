import wave

def get_wav_duration_seconds(filename: str) -> float:
    with wave.open(filename, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    return duration

def calculate_bpm(filename: str, beats_per_loop: int = 4) -> float:
    duration = get_wav_duration_seconds(filename)
    bpm = (beats_per_loop / duration) * 60
    return bpm

# Example usage
filename = 'samples/devils_lost.wav'
bpm = calculate_bpm(filename, beats_per_loop=4)  # adjust if it's 2 bars, etc.
print(f"Estimated BPM: {bpm:.2f}")

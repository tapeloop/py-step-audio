"""
Create a wrapped sequencer with trim and playback functionality. The principal settings are based around the original sample

"""
import sys
import os
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import pygame
import tempfile
import threading
from editor import WaveformTrimUI
from utils import calculate_bpm

pygame.mixer.init()

def play_audio(audio_segment):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
        audio_segment.export(f.name, format="wav")
        sound = pygame.mixer.Sound(f.name)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(100)

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


class StepSequencerApp(tk.Tk):
    def __init__(self, initial_wav=None):
        super().__init__()
        self.title("Step Sequencer with Trim and Playback")

        self.samples = [None] * 4
        self.grid_buttons = []
        self.pattern = [[False for _ in range(16)] for _ in range(4)]
        self.is_playing = False
        self.current_step = 0
        self.tempo = 120

        if initial_wav:
            audio = AudioSegment.from_wav(initial_wav)
            self.samples[0] = audio
            self.tempo = int(calculate_bpm(initial_wav))


        control_frame = tk.Frame(self)
        control_frame.pack(side='top', fill='x', padx=10)

        self.play_button = tk.Button(control_frame, text="Start", command=self.start_stop)
        self.play_button.pack(side='left', padx=5)
        
        tk.Label(control_frame, text="Tempo (BPM)").pack(side='left', padx=5)
        self.tempo_scale = tk.Scale(control_frame, from_=30, to=200, orient='horizontal')
        self.tempo_scale.set(self.tempo)
        self.tempo_scale.pack(side='left', padx=5)

        self.load_buttons = []

        grid_frame = tk.Frame(self)
        grid_frame.pack(padx=10, pady=10)

        for row in range(4):
            row_frame = tk.Frame(grid_frame)
            row_frame.pack(pady=5)

            button_panel = tk.Frame(row_frame)
            button_panel.pack(side='left', padx=5)

            load_btn = tk.Button(button_panel, text="Load", command=lambda i=row: self.load_sample(i))
            load_btn.pack()
            self.load_buttons.append(load_btn)

            tk.Button(button_panel, text="Trim", command=lambda i=row: self.trim_sample(i)).pack()
            tk.Button(button_panel, text="Preview", command=lambda i=row: self.play_sample(i)).pack()

            step_row = []
            step_panel = tk.Frame(row_frame)
            step_panel.pack(side='left')

            for col in range(16):
                var = tk.BooleanVar()
                chk = tk.Checkbutton(step_panel, variable=var)
                chk.pack(side='left')
                step_row.append(var)
            self.grid_buttons.append(step_row)

    def start_stop(self):
        if not self.is_playing:
            self.is_playing = True
            self.play_button.config(text="Stop")
            self.after(0, self.play_loop)
        else:
            self.is_playing = False
            self.play_button.config(text="Start")

    def trim_sample(self, index):
        if self.samples[index]:
            def on_trim(trimmed_audio):
                self.samples[index] = trimmed_audio
                print(f"Sample {index + 1} trimmed.")
            WaveformTrimUI(self, self.samples[index], on_trim)

    def play_sample(self, index):
        if self.samples[index]:
            threading.Thread(target=play_audio, args=(self.samples[index],), daemon=True).start()

    def start_stop(self):
        if not self.is_playing:
            self.is_playing = True
            self.play_button.config(text="Stop")
            self.after(0, self.play_loop)
        else:
            self.is_playing = False
            self.play_button.config(text="Start")

    def load_sample(self, index):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            audio = AudioSegment.from_wav(file_path)
            self.samples[index] = audio
            file_name = os.path.basename(file_path)
            self.load_buttons[index].config(text=file_name)
            print(f"Loaded sample {index + 1}")        
            
    def play_loop(self):
        if not self.is_playing:
            return

        for i in range(4):
            if self.grid_buttons[i][self.current_step].get():
                self.play_sample(i)

        self.current_step = (self.current_step + 1) % 16
        interval = int(60000 / self.tempo_scale.get() / 4)  # 16th notes
        self.after(interval, self.play_loop)



if __name__ == "__main__":
    initial_wav = sys.argv[1] if len(sys.argv) > 1 else None
    StepSequencerApp(initial_wav).mainloop()
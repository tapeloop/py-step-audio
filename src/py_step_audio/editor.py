import tkinter as tk
import numpy as np

from utils import play_audio


class WaveformTrimUI(tk.Toplevel):
    def __init__(self, master, audio_segment, on_trim_callback):
        super().__init__(master)
        self.audio = audio_segment
        self.on_trim = on_trim_callback

        self.title("Trim Sample")
        self.canvas_width = 600
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=100, bg="black")
        self.canvas.pack()

        self.samples = np.array(self.audio.get_array_of_samples())
        self.samples = self.samples[:: max(1, len(self.samples) // self.canvas_width)]

        self.start_pos = 0
        self.end_pos = len(self.samples)

        self.start_slider = tk.Scale(
            self,
            from_=0,
            to=len(self.samples),
            orient="horizontal",
            label="Start",
            command=self.update_start,
        )
        self.start_slider.pack(fill="x")

        self.end_slider = tk.Scale(
            self,
            from_=0,
            to=len(self.samples),
            orient="horizontal",
            label="End",
            command=self.update_end,
        )
        self.end_slider.set(len(self.samples))
        self.end_slider.pack(fill="x")

        btn_frame = tk.Frame(self)
        btn_frame.pack()

        tk.Button(btn_frame, text="Preview", command=self.preview).pack(side="left")
        tk.Button(btn_frame, text="Apply Trim", command=self.apply_trim).pack(
            side="left"
        )

        self.draw_waveform()

    def draw_waveform(self):
        self.canvas.delete("all")
        h = 100
        mid = h // 2
        scale = max(abs(self.samples.min()), self.samples.max())
        if scale == 0:
            scale = 1

        for i, s in enumerate(self.samples):
            y = int((s / scale) * mid)
            color = "lime"
            if i == self.start_pos or i == self.end_pos:
                color = "red"
            elif self.start_pos < i < self.end_pos:
                color = "yellow"
            self.canvas.create_line(i, mid - y, i, mid + y, fill=color)

    def update_start(self, val):
        self.start_pos = int(val)
        if self.start_pos >= self.end_pos:
            self.start_pos = self.end_pos - 1
            self.start_slider.set(self.start_pos)
        self.draw_waveform()

    def update_end(self, val):
        self.end_pos = int(val)
        if self.end_pos <= self.start_pos:
            self.end_pos = self.start_pos + 1
            self.end_slider.set(self.end_pos)
        self.draw_waveform()

    def preview(self):
        trimmed = self.trim_audio()
        play_audio(trimmed)

    def trim_audio(self):
        start_ms = (self.start_pos / len(self.samples)) * len(self.audio)
        end_ms = (self.end_pos / len(self.samples)) * len(self.audio)
        return self.audio[int(start_ms) : int(end_ms)]

    def apply_trim(self):
        trimmed = self.trim_audio()
        self.on_trim(trimmed)
        self.destroy()

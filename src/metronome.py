import threading
import time
import simpleaudio as sa
import numpy as np


class Metronome:
    def __init__(self, n_frames, bpm):
        self.bpm = bpm
        self.beats = np.zeros(n_frames, dtype=bool)
        self.high_beat = sa.WaveObject.from_wave_file("assets/sounds/metronome_hi.wav")
        self.low_beat = sa.WaveObject.from_wave_file("assets/sounds/metronome_lo.wav")
        self._output = False
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()
        
    def run(self):
        beat_interval = 60 / self.bpm
        while self.running:
            for i in range(4):
                if not self.running:
                    break
                if i == 0:
                    self.high_beat.play()
                else:
                    self.low_beat.play()
                self._output = True
                time.sleep(beat_interval)

    def update(self):
        self.beats[1:] = self.beats[:-1]
        self.beats[0] = self.output

    @property
    def output(self):
        if self._output:
            self._output = False
            return True
        return False
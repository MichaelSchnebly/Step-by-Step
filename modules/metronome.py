import threading
import time
import simpleaudio as sa


class Metronome:
    '''A metronome thread that plays a sound and triggers an output at a given BPM.
    '''
    def __init__(self, bpm):
        self.bpm = bpm

        self.high_beat = sa.WaveObject.from_wave_file("sounds/metronome_hi.wav")
        self.low_beat = sa.WaveObject.from_wave_file("sounds/metronome_lo.wav")
        self._output = False

        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        '''Plays a sound and triggers an output at a given BPM.'''
        beat_interval = 60 / self.bpm
        while True:
            for i in range(4):
                if i == 0:
                    self.high_beat.play()
                else:
                    self.low_beat.play()
                self._output = True
                time.sleep(beat_interval)

    @property
    def output(self):
        '''Returns the output state.'''
        if self._output:
            self._output = False
            print("Metronome triggered")
            return True
        return False
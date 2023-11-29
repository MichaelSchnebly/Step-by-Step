import time
import simpleaudio as sa

def play_metronome(bpm):
    high_beat = sa.WaveObject.from_wave_file("sounds/metronome_hi.wav")
    low_beat = sa.WaveObject.from_wave_file("sounds/metronome_lo.wav")
    
    beat_interval = 60 / bpm
    while True:
        for i in range(4):
            if i == 0:
                high_beat.play()
            else:
                low_beat.play()
            time.sleep(beat_interval)

# Example usage
play_metronome(120) # Uncomment to run the metronome at 120 BPM
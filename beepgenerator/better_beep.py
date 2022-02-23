import pyaudio
import numpy as np

p = pyaudio.PyAudio()

FS = 44100       # sampling rate, Hz, must be integer
FRAMES_PER_BUFFER = 64

class SineOsc:
    def __init__(self, freq, sample_rate, left_phase, right_phase):
        self.table_size = sample_rate/freq
        self.wave_table = []
        for i in range(self.table_size):
            self.wave_table.append(np.sin(i/self.table_size*np.pi*2))
        self.left_frame = 0
        self.right_frame = 0
        self.left_phase = left_phase
        self.right_phase = right_phase

    def next(self):
        table_len = len(self.wave_table)
        left = self.wave_table[self.left_frame]
        self.left_frame += self.left_phase
        if self.left_phase >= table_len:
            self.left_frame = self.left_frame - table_len

        right = self.wave_table[self.right_frame]
        self.right_frame += self.right_phase
        if self.right_phase >= table_len:
            self.right_frame = self.right_frame - table_len
        return self.left, self.right

def play(osc, duration, settings):
    pa = pyaudio.PyAudio()
    pa.open(format=pyaudio.paFloat32,
            channels=2,
            rate=FS,
            output=true,
            callback=osc)


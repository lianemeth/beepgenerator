import pyaudio
import numpy as np

p = pyaudio.PyAudio()

FS = 44100       # sampling rate, Hz, must be integer


def additive_synth(f, volumes, duration):
    duration = FS * duration
    streams = osc(volumes[0], f, duration)
    for i, vol in enumerate(volumes[1:]):
        streams += osc(vol, f*(i+1), duration)
    return streams.astype(np.float32).tobytes()


def osc(volume, f, duration):
    return volume * np.sin(2*np.pi*np.arange(duration)*f/FS)


osc_amp = [0.8, 0.7, 0.2, 0.4, 0.1, 0.9]
freq_dur = [(110, 0.6), (429.8, 0.9), (587.33, 0.4), (220, 0.2), (263.74, 0.1)]

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=FS,
                output=True)

for i in range(5):
    for freq, dur in freq_dur:
        stream.write(additive_synth(freq, osc_amp, dur))

stream.stop_stream()
stream.close()

p.terminate()

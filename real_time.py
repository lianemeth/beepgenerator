import pyaudio
import numpy as np
import time

p = pyaudio.PyAudio()
FS = 44100       # sampling rate, Hz, must be integer

envelope = []
for i in range(FS):
    if i >= 22100:
        envelope.append(0.8)
    else:
        envelope.append(0.5)
envelope = np.array(envelope)


sine_440 = (np.sin(2*np.pi*np.arange(FS)*440.0/FS)).astype(np.float32)
sine_880 = (envelope * np.sin(2*np.pi*np.arange(FS)*880.0/FS)).astype(np.float32)
table_size = len(sine_440)

PHASE = 0


def osc(freq, frame_count):
    global PHASE
    buffer = []
    for i in range(frame_count):
        PHASE += 1
        if PHASE >= table_size:
            PHASE = PHASE - table_size
        buffer.append(sine_440[PHASE] + sine_880[PHASE])
    return np.array(buffer).astype(np.float32)


def tunes(in_data, frame_count, time_info, flag):
    return (osc(440, frame_count), pyaudio.paContinue)


# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=FS,
                output=True,
                stream_callback=tunes)

while stream.is_active():
    time.sleep(10)
    stream.stop_stream()
stream.close()

p.terminate()

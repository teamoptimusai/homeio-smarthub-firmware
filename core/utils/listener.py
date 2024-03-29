'''
Get Audio frames from the microphone of the device
'''
import pyaudio
import wave
import collections

# listener defaults
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5


class Listener:
    def __init__(self, chunk_size=CHUNK_SIZE, format=FORMAT, n_channels=CHANNELS, sample_rate=RATE, record_seconds=RECORD_SECONDS):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=format, channels=n_channels,
                                  rate=sample_rate, input=True, frames_per_buffer=chunk_size)
        self.n_channels = n_channels
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.record_seconds = record_seconds
        self.frames = collections.deque(maxlen=int(
            sample_rate / chunk_size * record_seconds))

    def get_audio(self):
        self.frames = []
        for i in range(0, int(self.sample_rate / self.chunk_size * self.record_seconds)):
            data = self.stream.read(
                self.chunk_size, exception_on_overflow=False)
            self.frames.append(data)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def save_audio(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.n_channels)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.frames = []

    def save_audio_frames(self, frames, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.n_channels)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def get_frames(self):
        return list(self.frames)

    def get_audio_as_string(self):
        return b''.join(self.frames)

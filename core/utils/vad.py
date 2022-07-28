import wave
import webrtcvad
import collections
import pyaudio
from array import array
import time

from .misc import create_logger

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30       # supports 10, 20 and 30 (ms)
PADDING_DURATION_MS = 1500   # 1 sec jugement
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  # chunk to read
CHUNK_BYTES = CHUNK_SIZE * 2  # 16bit = 2 bytes, PCM
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)

NUM_WINDOW_CHUNKS = int(240 / CHUNK_DURATION_MS)
# NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)  # 400 ms/ 30ms  ge

NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2
START_OFFSET = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE)

logger = create_logger('VAD', 'homeio.log')


class VAD:
    def __init__(self):
        self.vad = webrtcvad.Vad(1)
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=RATE,
                                   input=True,
                                   start=False,
                                   # input_device_index=2,
                                   frames_per_buffer=CHUNK_SIZE)
        self.got_a_sentence = False
        logger.info('VAD initialized')

    def loop(self, callback):
        while True:
            ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)
            triggered = False
            ring_buffer_flags = [0] * NUM_WINDOW_CHUNKS
            ring_buffer_index = 0

            ring_buffer_flags_end = [0] * NUM_WINDOW_CHUNKS_END
            ring_buffer_index_end = 0

            raw_data = array('h')
            index = 0
            start_point = 0
            StartTime = time.time()
            self.stream.start_stream()

            while not self.got_a_sentence:
                chunk = self.stream.read(CHUNK_SIZE)
                raw_data.extend(array('h', chunk))
                index += CHUNK_SIZE
                TimeUse = time.time() - StartTime

                active = self.vad.is_speech(chunk, RATE)

                ring_buffer_flags[ring_buffer_index] = 1 if active else 0
                ring_buffer_index += 1
                ring_buffer_index %= NUM_WINDOW_CHUNKS

                ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
                ring_buffer_index_end += 1
                ring_buffer_index_end %= NUM_WINDOW_CHUNKS_END

                # start point detection
                if not triggered:
                    ring_buffer.append(chunk)
                    num_voiced = sum(ring_buffer_flags)
                    if num_voiced > 0.8 * NUM_WINDOW_CHUNKS:
                        triggered = True
                        start_point = index - CHUNK_SIZE * 20  # start point
                        ring_buffer.clear()
                # end point detection
                else:
                    ring_buffer.append(chunk)
                    num_unvoiced = NUM_WINDOW_CHUNKS_END - \
                        sum(ring_buffer_flags_end)

                    if num_unvoiced > 0.90 * NUM_WINDOW_CHUNKS_END or TimeUse > 10:
                        triggered = False
                        self.got_a_sentence = True

            self.stream.stop_stream()
            logger.info('Speech Detected')
            self.got_a_sentence = False

            # write to file
            raw_data.reverse()
            for index in range(start_point):
                raw_data.pop()

            raw_data.reverse()
            raw_data = self.normalize(raw_data)
            wav_data = raw_data[44:len(raw_data)]
            # convert to bytes
            wav_data = array('h', wav_data)
            wav_data = wave.struct.pack('h' * len(wav_data), *wav_data)
            # write to a wav file
            wf = wave.open('output.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.pa.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(wav_data)
            wf.close()
            callback('output.wav')

    @staticmethod
    def normalize(snd_data):
        MAXIMUM = 32767  # 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)
        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r

    def close(self):
        self.stream.close()


if __name__ == "__main__":
    vad = VAD()
    vad.loop(lambda x: print(x))

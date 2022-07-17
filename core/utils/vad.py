import webrtcvad
import collections
import sys

from .listener import Listener
from .misc import write_wave, read_wave, frame_generator, Frame


class VAD:
    def __init__(self, sample_rate: int, frame_duration_ms: int, padding_duration_ms: int, debug: bool = False):
        self.vad = webrtcvad.Vad(mode=1)
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.padding_duration_ms = padding_duration_ms
        self.debug = debug

    def is_speech(self, frame: Frame):
        return self.vad.is_speech(frame.bytes, self.sample_rate)

    def collector(self, frames: list[Frame]):
        num_padding_frames = int(
            self.padding_duration_ms / self.frame_duration_ms)
        ring_buffer = collections.deque(maxlen=num_padding_frames)

        triggered = False
        voiced_frames = []

        for frame in frames:
            is_speech = self.is_speech(frame)

            if self.debug:
                sys.stdout.write('1' if is_speech else '0')

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced > 0.9 * ring_buffer.maxlen:
                    triggered = True

                    if self.debug:
                        sys.stdout.write('+(%s)' % (frame.timestamp,))

                    for f, s in ring_buffer:
                        voiced_frames.append(f)
                    ring_buffer.clear()
            else:
                voiced_frames.append(frame)
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len(
                    [f for f, speech in ring_buffer if not speech])
                if num_unvoiced > 0.9 * ring_buffer.maxlen:
                    if self.debug:
                        sys.stdout.write('-(%s)' %
                                         (frame.timestamp + frame.duration))
                    triggered = False
                    yield b''.join([f.bytes for f in voiced_frames])
                    ring_buffer.clear()
                    voiced_frames = []

        if triggered & self.debug:
            sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
        if voiced_frames:
            yield b''.join([f.bytes for f in voiced_frames])

    def process(self, path: str, save: bool = False):
        audio, sample_rate, n_channels = read_wave(path)
        assert n_channels == 1
        frames = frame_generator(self.frame_duration_ms, audio, sample_rate)
        frames = list(frames)
        segments = self.collector(frames)
        if save:
            for i, segments in enumerate(segments):
                write_wave('chunk_%002d.wav' % (i,), segments, sample_rate)
        else:
            segments = list(segments)
        return segments


if __name__ == '__main__':
    from listener import Listener

    listener = Listener(n_channels=1, record_seconds=10, sample_rate=16000)
    vad = VAD(sample_rate=16000, frame_duration_ms=30, padding_duration_ms=300)

    for x in range(1):
        listener.get_audio()
        listener.save_audio(f'test{x}.wav')
        vad.process(f'test{x}.wav', save=True)

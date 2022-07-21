import time
import playsound

from utils.listener import Listener
from utils.vad import VAD
from utils.speech2text import Speech2Text
from utils.nlu import NLUEngine
from utils.config import NLU_CONFIG, WAKEWORD, SAMPLE_RATE, RECORD_SECONDS, FRAME_DURATION_MS, PADDING_DURATION_MS


class SpeechRecognition:
    def __init__(self, sample_rate, frame_duration_ms, padding_duration_ms, debug=False):
        sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.padding_duration_ms = padding_duration_ms

        start = time.time()
        self.listener = Listener(n_channels=1, record_seconds=RECORD_SECONDS,
                                 sample_rate=sample_rate,)
        self.vad = VAD(self.sample_rate, self.frame_duration_ms,
                       self.padding_duration_ms, debug)
        print('Listner and VAD Initialized. Time taken: {}'.format(
            time.time() - start))

    def loop(self, callback):
        while True:
            self.listener.get_audio()
            self.listener.save_audio('temp.wav')
            segments = self.vad.process('temp.wav')
            segments = list(segments)
            if len(segments):
                print("Speech detected!")
                chunks = self.vad.save(segments)

                start = time.time()
                speech2text = Speech2Text()
                print('Speech2Text Initialized. Time taken: {}'.format(
                    time.time() - start))

                for chunk in chunks:
                    sentence = speech2text.recognize('test.wav')
                    if WAKEWORD in sentence:
                        playsound.playsound('welcome.mp3')
                        self.listener.get_audio(record_seconds=4)
                        self.listener.save_audio('command.wav')
                        callback(speech2text.recognize('command.wav'))


def command_callback(sentence):
    nlu = NLUEngine(NLU_CONFIG)
    print(nlu.predict(sentence))


if __name__ == "__main__":
    asr = SpeechRecognition(SAMPLE_RATE, FRAME_DURATION_MS,
                            PADDING_DURATION_MS, False)
    asr.loop(callback=command_callback)

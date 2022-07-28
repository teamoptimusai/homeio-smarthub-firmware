import threading

from utils.misc import write_wave_frames, create_logger
from utils.listener import Listener
from utils.vad import VAD
from utils.config import FRAME_DURATION_MS, PADDING_DURATION_MS, SAMPLE_RATE, WINDOW_SIZE, MAX_NOSPEECH, NLU_CONFIG, WAKEWORDS
from utils.speech2text import Wav2Vec2_transformer
from utils.nlu import NLUEngine
from utils.controller import Controller

# initialize a logger with timestamp
logger = create_logger('Main', 'homeio.log')
frames = []


class ListnerThread(threading.Thread):
    def __init__(self, sample_rate):
        threading.Thread.__init__(self)
        self.listener = Listener(n_channels=1, record_seconds=1,
                                 sample_rate=sample_rate,)

    def collect_audio(self):
        while True:
            self.listener.get_audio()
            collected_frames = self.listener.get_frames()
            frames.extend(collected_frames)

    def run(self):
        logger.info('Listner Thread started')
        self.collect_audio()


def speech_callback():
    sentence = stt.transcribe('command.wav')
    logger.info('Speech detected! Sentence: ' + sentence)
    if sentence.split()[0] in WAKEWORDS:
        logger.info('Wakeword detected!')
        output = nlu.predict(sentence)
        logger.info('Output: {}'.format(output))
        controller.parse(output)


try:
    listner_thread = ListnerThread(SAMPLE_RATE)
    listner_thread.start()

    vad = VAD(SAMPLE_RATE, FRAME_DURATION_MS, PADDING_DURATION_MS, False)
    nlu = NLUEngine(NLU_CONFIG)
    controller = Controller()
    stt = Wav2Vec2_transformer()

    print("Automatic Speech Recognition Started... Press Ctrl+C Twice to exit")

    speech_frames = []
    n_nospeech_frames = 0
    start = 0
    while True:
        if len(frames) >= WINDOW_SIZE:
            write_wave_frames('temp.wav', frames[start:start+WINDOW_SIZE])
            segments = vad.process('temp.wav')
            segments = list(segments)
            if len(segments):
                speech_frames.extend(frames[start:start+WINDOW_SIZE])
                start += WINDOW_SIZE
            elif len(speech_frames):
                n_nospeech_frames += 1
                if (n_nospeech_frames > MAX_NOSPEECH) or (len(speech_frames)/SAMPLE_RATE > 3):
                    write_wave_frames('command.wav', speech_frames)
                    speech_callback()
                    speech_frames = []
                    frames = []
                    start = 0
                    n_nospeech_frames = 0
                else:
                    speech_frames.extend(frames[start:start+WINDOW_SIZE])
                    frames = frames[start+WINDOW_SIZE:]
                    start = 0
            else:
                frames = frames[start+WINDOW_SIZE:]
                start = 0
except KeyboardInterrupt:
    logger.info('Keyboard Interrupt')
    listner_thread.listener.close()
    listner_thread.join()
    logger.info('Listner Thread stopped')
    logger.info('Exiting')
    exit(0)
except Exception as e:
    logger.error(e)
    listner_thread.listener.close()
    listner_thread.join()
    logger.info('Listner Thread stopped')
    logger.info('Exiting')
    exit(0)

from utils.misc import create_logger
from utils.config import NLU_CONFIG, WAKEWORDS
from utils.speech2text import Wav2Vec2_transformer
from utils.nlu import NLUEngine
from utils.controller import Controller
from utils.vad import VAD

# initialize a logger with timestamp
logger = create_logger('Main', 'homeio.log')


def speech_callback(filename):
    sentence = stt.transcribe(filename)
    words = sentence.split()
    if len(words) > 0:
        logger.info('Speech detected! Sentence: ' + sentence)
        if sentence.split()[0] in WAKEWORDS:
            logger.info('Wakeword detected!')
            output = nlu.predict(sentence)
            logger.info('Output: {}'.format(output))
            controller.parse(output)


try:
    vad = VAD()
    nlu = NLUEngine(NLU_CONFIG)
    controller = Controller()
    stt = Wav2Vec2_transformer()

    print("Automatic Speech Recognition Started... Press Ctrl+C Twice to exit")
    vad.loop(speech_callback)

except KeyboardInterrupt:
    logger.info('Keyboard Interrupt')
    logger.info('Exiting')
    exit(0)
except Exception as e:
    logger.error(e)
    logger.info('Exiting')
    exit(0)

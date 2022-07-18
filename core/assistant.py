import argparse

from utils.listener import Listener
from utils.vad import VAD
from utils.speech2text import Speech2Text
# from utils.hotword import HotwordDetector
from utils.nlu import NLUEngine, DEFAULT_CONFIG

WAKEWORD = 'hey google'
NLU_CONFIG = {
    **DEFAULT_CONFIG,
    'METADATA_LOCATION': 'core/models/nlu/metadata.bin',
    'WEIGHTS_LOCATION': 'core/models/nlu/epoch50_best_model_trace.pth',
}


class SpeechRecognition:
    def __init__(self):
        listener = Listener(n_channels=1, record_seconds=1,
                        sample_rate=args.sample_rate,)


def main():
    listener = Listener(n_channels=1, record_seconds=1,
                        sample_rate=args.sample_rate,)
    vad = VAD(args.sample_rate, args.frame_duration_ms,
              args.padding_duration_ms, debug=args.debug)
    # hotword_detector = HotwordDetector()

    while True:
        listener.get_audio()
        listener.save_audio('temp.wav')
        segments = vad.process('temp.wav')
        segments = list(segments)
        if len(segments):
            print("Speech detected!", len(segments))
            chunks = vad.save(segments)
            speech2text = Speech2Text()
            for chunk in chunks:
                sentence = speech2text.recognize(chunk)
                if sentence == WAKEWORD:
                    print('Hotword detected!')
                    nlu = NLUEngine(config=NLU_CONFIG)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true",
                        help="enable debug mode")
    parser.add_argument("--sample_rate", type=int,
                        default=16000, help="sample rate")
    parser.add_argument("--frame_duration_ms", type=int,
                        default=30, help="frame duration")
    parser.add_argument("--padding_duration_ms", type=int,
                        default=300, help="padding duration")
    args = parser.parse_args()

    # args.debug = True
    main()

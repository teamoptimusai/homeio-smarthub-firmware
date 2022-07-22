import speech_recognition as sr
from itertools import groupby
import json
from pathlib import Path
import numpy as np
import wave
from openvino.runtime import Core, PartialShape

DEFAULT_CONFIG = {
    'XML_PATH': 'core/models/speech2text/wav2vec2-base.xml',
    'DEVICE': 'CPU',
}


class CMUSphinx:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize(self, audio):
        with sr.AudioFile(audio) as source:
            audio = self.recognizer.record(source)
        try:
            return self.recognizer.recognize_sphinx(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that"


class Speech2Text:
    alphabet = [
        "<pad>", "<s>", "</s>", "<unk>", "|",
        "e", "t", "a", "o", "n", "i", "h", "s", "r", "d", "l", "u",
        "m", "w", "c", "f", "g", "y", "p", "b", "v", "k", "'", "x", "j", "q", "z"]
    words_delimiter = '|'
    pad_token = '<pad>'

    def __init__(self, core, model_path, input_shape, device, vocab_file, dynamic_flag):
        model = core.read_model(model_path)
        self.input_tensor_name = model.inputs[0].get_any_name()
        if not dynamic_flag:
            model.reshape({self.input_tensor_name: PartialShape(input_shape)})
        elif not model.is_dynamic():
            model.reshape({self.input_tensor_name: PartialShape((-1, -1))})
        compiled_model = core.compile_model(model, device)
        self.output_tensor = compiled_model.outputs[0]
        self.infer_request = compiled_model.create_infer_request()
        self._init_vocab(vocab_file)

    def _init_vocab(self, vocab_file):
        if vocab_file is not None:
            vocab_file = Path(vocab_file)
            with vocab_file.open('r') as vf:
                encoding_vocab = json.load(vf)
                self.decoding_vocab = {
                    int(v): k for k, v in encoding_vocab.items()}
                return
        self.decoding_vocab = dict(enumerate(self.alphabet))

    @staticmethod
    def preprocess(sound):
        return (sound - np.mean(sound)) / (np.std(sound) + 1e-15)

    def infer(self, audio):
        input_data = {self.input_tensor_name: audio}
        return self.infer_request.infer(input_data)[self.output_tensor]

    def decode(self, logits):
        token_ids = np.squeeze(np.argmax(logits, -1))
        tokens = [self.decoding_vocab[idx] for idx in token_ids]
        tokens = [token_group[0] for token_group in groupby(tokens)]
        tokens = [t for t in tokens if t != self.pad_token]
        res_string = ''.join(
            [t if t != self.words_delimiter else ' ' for t in tokens]).strip()
        res_string = ' '.join(res_string.split(' '))
        res_string = res_string.lower()
        return res_string


def transcribe(wavfile, config):
    with wave.open(wavfile, 'rb') as wave_read:
        channel_num, _, _, pcm_length, _, _ = wave_read.getparams()
        audio = np.frombuffer(wave_read.readframes(
            pcm_length * channel_num), dtype=np.int16).reshape((1, pcm_length))
        audio = audio.astype(float) / np.iinfo(np.int16).max

    core = Core()
    model = Speech2Text(core, config['XML_PATH'],
                        audio.shape, config['DEVICE'], None, False)
    normalized_audio = model.preprocess(audio)
    character_probs = model.infer(normalized_audio)
    transcription = model.decode(character_probs)
    return transcription


if __name__ == "__main__":
    print(CMUSphinx().recognize('command.wav'))
    import time
    start = time.time()
    print(transcribe('command.wav', DEFAULT_CONFIG))
    print(time.time() - start)

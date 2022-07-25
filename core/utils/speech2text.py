import speech_recognition as sr
# from itertools import groupby
# import json
# from pathlib import Path
# import numpy as np
# import wave
# from openvino.runtime import Core, PartialShape
import transformers
import soundfile as sf
import torch
from .misc import create_logger

DEFAULT_CONFIG = {
    'XML_PATH': 'core/models/speech2text/wav2vec2-base.xml',
    'DEVICE': 'CPU',
}

logger = create_logger('STT', 'homeio.log')


class CMUSphinx:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize(self, audio):
        with sr.AudioFile(audio) as source:
            audio = self.recognizer.record(source)
        try:
            return self.recognizer.recognize_sphinx(audio)
        except Exception as e:
            logger.error(e)
            return "Sorry, I didn't catch that"


# class Wav2Vec2_OpenVINO:
    # alphabet = [
    #     "<pad>", "<s>", "</s>", "<unk>", "|",
    #     "e", "t", "a", "o", "n", "i", "h", "s", "r", "d", "l", "u",
    #     "m", "w", "c", "f", "g", "y", "p", "b", "v", "k", "'", "x", "j", "q", "z"]
    # words_delimiter = '|'
    # pad_token = '<pad>'

    # def __init__(self, core, model_path, input_shape, device, vocab_file, dynamic_flag):
    #     model = core.read_model(model_path)
    #     self.input_tensor_name = model.inputs[0].get_any_name()
    #     if not dynamic_flag:
    #         model.reshape({self.input_tensor_name: PartialShape(input_shape)})
    #     elif not model.is_dynamic():
    #         model.reshape({self.input_tensor_name: PartialShape((-1, -1))})
    #     compiled_model = core.compile_model(model, device)
    #     self.output_tensor = compiled_model.outputs[0]
    #     self.infer_request = compiled_model.create_infer_request()
    #     self._init_vocab(vocab_file)

    # def _init_vocab(self, vocab_file):
    #     if vocab_file is not None:
    #         vocab_file = Path(vocab_file)
    #         with vocab_file.open('r') as vf:
    #             encoding_vocab = json.load(vf)
    #             self.decoding_vocab = {
    #                 int(v): k for k, v in encoding_vocab.items()}
    #             return
    #     self.decoding_vocab = dict(enumerate(self.alphabet))

    # @staticmethod
    # def preprocess(sound):
    #     return (sound - np.mean(sound)) / (np.std(sound) + 1e-15)

    # def infer(self, audio):
    #     input_data = {self.input_tensor_name: audio}
    #     return self.infer_request.infer(input_data)[self.output_tensor]

    # def decode(self, logits):
    #     token_ids = np.squeeze(np.argmax(logits, -1))
    #     tokens = [self.decoding_vocab[idx] for idx in token_ids]
    #     tokens = [token_group[0] for token_group in groupby(tokens)]
    #     tokens = [t for t in tokens if t != self.pad_token]
    #     res_string = ''.join(
    #         [t if t != self.words_delimiter else ' ' for t in tokens]).strip()
    #     res_string = ' '.join(res_string.split(' '))
    #     res_string = res_string.lower()
    #     return res_string

class Wav2Vec2_transformer:
    def __init__(self):
        model_name = "facebook/wav2vec2-base-960h"
        self.tokenizer = transformers.Wav2Vec2Tokenizer.from_pretrained(
            model_name)  # omdel_name
        self. model = transformers.Wav2Vec2ForCTC.from_pretrained(model_name)

    def transcribe(self, audio):
        data, sr = sf.read(audio)
        try:
            input_values = self.tokenizer(
                data, return_tensors='pt').input_values
            logits = self.model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcriptions = self.tokenizer.decode(predicted_ids[0]).lower()
            return transcriptions
        except Exception as e:
            logger.error(e)
            return "Sorry, I didn't catch that"


# def transcribe_wav2vec_openvino(wavfile, config):
#     with wave.open(wavfile, 'rb') as wave_read:
#         channel_num, _, _, pcm_length, _, _ = wave_read.getparams()
#         audio = np.frombuffer(wave_read.readframes(
#             pcm_length * channel_num), dtype=np.int16).reshape((1, pcm_length))
#         audio = audio.astype(float) / np.iinfo(np.int16).max

#     core = Core()
#     model = Wav2Vec(core, config['XML_PATH'],
#                         audio.shape, config['DEVICE'], None, False)
#     normalized_audio = model.preprocess(audio)
#     character_probs = model.infer(normalized_audio)
#     transcription = model.decode(character_probs)
    # return transcription


def transcribe_sphinx(wavfile):
    sphinx = CMUSphinx()
    return sphinx.recognize(wavfile)


if __name__ == "__main__":
    print(CMUSphinx().recognize('command.wav'))
    # print(transcribe_wav2vec('command.wav', DEFAULT_CONFIG))

from utils.nlu import DEFAULT_CONFIG as NLU_DEFAULT_CONFIG
from utils.speech2text import DEFAULT_CONFIG as STT_DEFAULT_CONFIG

WAKEWORDS = ['hello', 'hi', 'hey', 'hillo']

# nlu Configurations
NLU_CONFIG = {
    **NLU_DEFAULT_CONFIG,
    'METADATA_LOCATION': 'core/models/nlu/metadata.bin',
    'WEIGHTS_LOCATION': 'core/models/nlu/epoch50_best_model_trace.pth',
}

# Speech to text Configurations
STT_CONFIG = {
    **STT_DEFAULT_CONFIG,
    'XML_PATH': 'core/models/speech2text/wav2vec2-base.xml',
    'DEVICE': 'CPU',
}

# Listner defaults
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
RECORD_SECONDS = 1

# vad configurations
FRAME_DURATION_MS = 30
PADDING_DURATION_MS = 300

# Text2Speech Configurations
LANGUAGE = 'en'

# ASR Configurations
WINDOW_SIZE = 15
MAX_NOSPEECH = 4

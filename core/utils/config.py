from utils.nlu import DEFAULT_CONFIG

WAKEWORD = 'hello'

#nlu Configurations
NLU_CONFIG = {
    **DEFAULT_CONFIG,
    'METADATA_LOCATION': 'core/models/nlu/metadata.bin',
    'WEIGHTS_LOCATION': 'core/models/nlu/epoch50_best_model_trace.pth',
}

#Listner defaults
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
RECORD_SECONDS = 1

#vad configurations
FRAME_DURATION_MS = 30
PADDING_DURATION_MS = 300

#Text2Speech Configurations
LANGUAGE = 'en'

#ASR Configurations
WINDOW_SIZE = 15
MAX_NOSPEECH = 4
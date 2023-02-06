import os
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"

with open(ROOT_DIR + "config.yaml") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)
    AUDIO_SETTINGS = "audio_settings"
    DIRECTORY_SETTINGS = "directory_settings"
    AUDIO_VISUALIZER_SETTINGS = "audio_visualizer_settings"
    AUDIO_SPLITTER_SETTINGS = "audio_splitter_settings"
    SEPARATOR_SETTINGS = "separator_settings"
    DIARIZATION_SETTINGS = "diarization_settings"

    DEFAULT_AUDIO_SAMPLERATE = config[AUDIO_SETTINGS]["default_samplerate"]
    DEFAULT_AUDIO_OFFSET = config[AUDIO_SETTINGS]["default_offset"]
    DEFAULT_AUDIO_DURATION = config[AUDIO_SETTINGS]["default_duration"]

    MAIN_INPUT_DIR = config[DIRECTORY_SETTINGS]["main_input_directory"]
    AUDIO_DIR = config[DIRECTORY_SETTINGS]["audio_directory"]
    TEXT_DIR = config[DIRECTORY_SETTINGS]["text_directory"]
    PATIENTS_DIR = config[DIRECTORY_SETTINGS]["patient_directory"]
    SPLIT_AUDIO_DIR = config[DIRECTORY_SETTINGS]["split_audio_directory"]
    SPECTRUM_DIR = config[DIRECTORY_SETTINGS]["spectrum_audio_directory"]
    WAVEFORM_DIR = config[DIRECTORY_SETTINGS]["waveform_audio_directory"]
    FUNDAMENTAL_FREQUENCY_DIR = config[DIRECTORY_SETTINGS]["fundamental_frequency_audio_directory"]
    MAIN_OUTPUT_DIR = config[DIRECTORY_SETTINGS]["main_output_directory"]
    SEPFORMER_OUTPUT_DIR = config[DIRECTORY_SETTINGS]["sepformer_output_directory"]
    DIARIZATION_OUTPUT_DIR = config[DIRECTORY_SETTINGS]["diarization_output_directory"]

    SHOW_WAVEFORM = config[AUDIO_VISUALIZER_SETTINGS]["waveform"]
    SHOW_SPECTRUM = config[AUDIO_VISUALIZER_SETTINGS]["spectrum"]
    SHOW_MELSPECTROGRAM = config[AUDIO_VISUALIZER_SETTINGS]["mel_spectrogram"]
    SHOW_FUNDAMENTAL_FREQUENCY = config[AUDIO_VISUALIZER_SETTINGS]["fundamental_frequency"]

    SPLIT_ALL = config[AUDIO_SPLITTER_SETTINGS]["perform_all"]
    SPLITTER_IDS = tuple(config[AUDIO_SPLITTER_SETTINGS]["perform_on_ids"])
    SPLITTER_OFFSET = config[AUDIO_SPLITTER_SETTINGS]["offset"]
    SPLITTER_DURATION = config[AUDIO_SPLITTER_SETTINGS]["duration"]

    SEPARATOR_ALL = config[SEPARATOR_SETTINGS]["perform_all"]
    SEPARATOR_IDS = tuple(config[SEPARATOR_SETTINGS]["perform_on_ids"])

    DIARIZATION_ALL = config[DIARIZATION_SETTINGS]["perform_all"]
    DIARIZATION_IDS = tuple(config[DIARIZATION_SETTINGS]["perform_on_ids"])
    DIARIZATION_MODEL_OUTPUT_ORIGINAL = config[DIARIZATION_SETTINGS]["model_output"]["original"]
    DIARIZATION_MODEL_OUTPUT_SIZING = config[DIARIZATION_SETTINGS]["model_output"]["sizing"]

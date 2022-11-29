import os
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"

with open(ROOT_DIR + "config.yaml") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)
    AUDIO_SETTINGS = "audio_settings"
    DIRECTORY_SETTINGS = "directory_settings"
    AUDIO_VISUALIZER_SETTINGS = "audio_visualizer_settings"

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
    MAIN_OUTPUT_DIR = config[DIRECTORY_SETTINGS]["main_output_directory"]
    MASTER_OUTPUT_DIR = config[DIRECTORY_SETTINGS]["master_output_directory"]

    SHOW_WAVEFORM = config[AUDIO_VISUALIZER_SETTINGS]["waveform"]
    SHOW_SPECTRUM = config[AUDIO_VISUALIZER_SETTINGS]["spectrum"]
    SHOW_MELSPECTROGRAM = config[AUDIO_VISUALIZER_SETTINGS]["mel_spectrogram"]


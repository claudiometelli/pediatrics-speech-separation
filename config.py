import os
from configparser import ConfigParser

config = ConfigParser()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
config.read(ROOT_DIR + "/config.ini")

DEFAULT_AUDIO_SAMPLERATE = int(config["AUDIO_SETTINGS"]["DefaultSamplerate"])
DEFAULT_AUDIO_OFFSET = float(config["AUDIO_SETTINGS"]["DefaultOffset"])
DEFAULT_AUDIO_DURATION = None

MAIN_INPUT_DIR = config["DIRECTORY_SETTINGS"]["MainInputDirectory"]
AUDIO_DIR = config["DIRECTORY_SETTINGS"]["AudioDirectory"]
TEXT_DIR = config["DIRECTORY_SETTINGS"]["TextDirectory"]
PATIENTS_DIR = config["DIRECTORY_SETTINGS"]["PatientDirectory"]
SPLIT_AUDIO_DIR = config["DIRECTORY_SETTINGS"]["SplitAudioDirectory"]
SPECTRUM_DIR = config["DIRECTORY_SETTINGS"]["SpectrumAudioDirectory"]
TIME_SERIES_DIR = config["DIRECTORY_SETTINGS"]["TimeSeriesAudioDirectory"]
MAIN_OUTPUT_DIR = config["DIRECTORY_SETTINGS"]["MainOutputDirectory"]
MASTER_OUTPUT_DIR = config["DIRECTORY_SETTINGS"]["MasterOutputDirectory"]

SHOW_TIME_SERIES = True if config["AUDIO_VISUALIZER_SETTINGS"]["TimeSeries"] == "True" else False
SHOW_FULL_SPECTRUM = True if config["AUDIO_VISUALIZER_SETTINGS"]["FullSpectrum"] == "True" else False

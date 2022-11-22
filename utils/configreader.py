from configparser import ConfigParser

config = ConfigParser()
config.read("../config.ini")

default_audio_samplerate = int(config["AUDIO_SETTINGS"]["DefaultSamplerate"])
default_audio_offset = float(config["AUDIO_SETTINGS"]["DefaultOffset"])
default_audio_duration = None

main_input_directory = config["DIRECTORY_SETTINGS"]["MainInputDirectory"]
patients_directory = config["DIRECTORY_SETTINGS"]["PatientDirectory"]
split_audio_directory = config["DIRECTORY_SETTINGS"]["SplitAudioDirectory"]
main_output_directory = config["DIRECTORY_SETTINGS"]["MainOutputDirectory"]
master_output_directory = config["DIRECTORY_SETTINGS"]["MasterOutputDirectory"]

import os
import utils.audioutils as utils
from utils.configreader import main_input_directory, patients_directory, split_audio_directory
from utils.textreader import get_patient

# Get patient name
patient = get_patient()
patient_directory = patient.replace(" ", "_") + "/"

# Set input directories
input_file_path = patient + ".wav"
input_path = "../" + main_input_directory + patients_directory + patient_directory + input_file_path

# Set output directories and create if doesn't exist
if not os.path.exists("../" + main_input_directory + patients_directory + patient_directory + split_audio_directory):
    os.mkdir("../" + main_input_directory + patients_directory + patient_directory + split_audio_directory)
output_file_path = patient.replace(" ", "_")
output_path = "../" + main_input_directory + patients_directory + patient_directory + split_audio_directory + output_file_path

# Set params and read
offset, duration = 1, 19
output_audio = utils.load_audio(input_path, offset=offset, audio_duration=duration)

# Set output path and write
final_output_path = output_path + "_" + str(offset) + "_" + str(offset + duration) + ".wav"
utils.write_audio(final_output_path, output_audio)

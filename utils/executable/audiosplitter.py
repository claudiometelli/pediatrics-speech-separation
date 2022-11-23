import os
import utils.audioutils as audioutils
from config import ROOT_DIR, MAIN_INPUT_DIR, AUDIO_DIR, PATIENTS_DIR, SPLIT_AUDIO_DIR
from utils.textreader import get_patient

if __name__ == "__main__":
    # Get patient name and directory name
    patient = get_patient()
    patient_directory = patient.replace(" ", "_") + "/"

    # Set params and read
    offset, duration = 1, 20

    # Set input directories
    input_file_path = patient + ".wav"
    input_path = ROOT_DIR + MAIN_INPUT_DIR + AUDIO_DIR + PATIENTS_DIR + patient_directory + input_file_path

    # Set output directories and create if doesn't exist
    output_dir = ROOT_DIR + MAIN_INPUT_DIR + PATIENTS_DIR + patient_directory + SPLIT_AUDIO_DIR
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_path = patient.replace(" ", "_") + "_" + str(offset) + "_" + str(offset + duration) + ".wav"

    # Get audio
    output_audio = audioutils.load_audio(input_path, offset=offset, audio_duration=duration)

    # Set output path and write
    audioutils.write_audio(output_path, output_audio)

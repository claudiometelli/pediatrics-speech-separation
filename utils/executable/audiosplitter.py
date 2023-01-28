import os
import utils.audioutils as audioutils
from config import SPLIT_AUDIO_DIR, SPLIT_ALL, SPLITTER_IDS, SPLITTER_OFFSET, SPLITTER_DURATION
from utils.ioutils import get_patients_name, get_patients_directory_path, get_patient_name_by_id, get_patient_directory_path_by_id

if __name__ == "__main__":
    # Set params and read
    offset, duration = SPLITTER_OFFSET, SPLITTER_DURATION

    # Get patients name and path from config
    patients = {}
    if SPLIT_ALL:
        patient_paths = zip(get_patients_name(), get_patients_directory_path())
    else:
        names = [get_patient_name_by_id(patient_id) for patient_id in SPLITTER_IDS]
        paths = [get_patient_directory_path_by_id(patient_id) for patient_id in SPLITTER_IDS]
        patient_paths = zip(names, paths)

    # Set input file and output file for each patient
    patients = {patient: {
        "input_file": f"{path}{patient}.wav",
        "output_directory": f"{path}{SPLIT_AUDIO_DIR}",
        "output_file": f"{path}{SPLIT_AUDIO_DIR}{patient}_{SPLITTER_OFFSET}_{offset + duration}.wav"
    } for patient, path in patient_paths}

    # Create audio for each patient
    for patient, paths in patients.items():
        # Create output directories if doesn't exist
        if not os.path.exists(paths.get("output_directory")):
            os.mkdir(paths.get("output_directory"))
        # Get audio
        output_audio = audioutils.load_audio(paths.get("input_file"), offset=offset, audio_duration=duration)
        # Set output path and write
        audioutils.write_audio(paths.get("output_file"), output_audio)

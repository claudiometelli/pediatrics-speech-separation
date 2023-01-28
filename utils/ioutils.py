import os
from config import ROOT_DIR, MAIN_INPUT_DIR, MAIN_OUTPUT_DIR, AUDIO_DIR, PATIENTS_DIR, DIARIZATION_OUTPUT_DIR


def get_patients_name() -> list:
    """
    Methods to get names of all patients reading from their directories in file system
    :return: a list containing the names of all patients
    """
    input_path = ROOT_DIR + MAIN_INPUT_DIR + AUDIO_DIR + PATIENTS_DIR
    patients = [directory.replace("_", " ") for directory in os.listdir(input_path) if not directory.startswith("_")]
    return patients


def get_patients_directory_path() -> list:
    """
    Method to get directory path in file system for each patient
    :return: a list containing the directory path of all patients
    """
    input_path = ROOT_DIR + MAIN_INPUT_DIR + AUDIO_DIR + PATIENTS_DIR
    directories = [input_path + directory + "/" for directory in os.listdir(input_path) if not directory.startswith("_")]
    return directories


def get_patient_name_by_id(patient_id: int) -> str:
    """
    Return the name of a patient starting from a single id,
    which is the position in the list retrieved from get_patients_name(),
    so the nth in the alphabetic order of the patients
    :param patient_id: the patient id
    :return: the name of the patient
    """
    patient_names = get_patients_name()
    assert patient_id < len(patient_names), f"Patient with id {patient_id} does not exists"
    return patient_names[patient_id]


def get_patient_directory_path_by_id(patient_id) -> str:
    """
    Return the directory path of a patient starting from a single id,
    which is the position in the list retrieved from get_patients_directory_path(),
    so the nth in the alphabetic order of the patients
    :param patient_id: the patient id
    :return: the directory path of the patient
    """
    patient_directory_paths = get_patients_directory_path()
    assert patient_id < len(patient_directory_paths), f"Patient with id {patient_id} does not exists"
    return patient_directory_paths[patient_id]


def get_patients_audio_path() -> list:
    patients = get_patients_name()
    input_path = ROOT_DIR + MAIN_INPUT_DIR + AUDIO_DIR + PATIENTS_DIR
    directories = {patient: patient.replace(" ", "_") + "/" for patient in patients}
    paths = [input_path + directories.get(directory) + directory + ".wav" for directory in directories]
    return paths


def get_input_output_diarization_paths() -> dict:
    patients = get_patients_name()
    input_path = ROOT_DIR + MAIN_INPUT_DIR + AUDIO_DIR + PATIENTS_DIR
    output_path = ROOT_DIR + MAIN_OUTPUT_DIR + AUDIO_DIR + PATIENTS_DIR
    directories = {patient: patient.replace(" ", "_") + "/" for patient in patients}
    input_paths = [input_path + directories.get(patient) + patient + ".wav" for patient in directories]
    output_paths = [output_path + directories.get(patient) + DIARIZATION_OUTPUT_DIR + patient for patient in directories]
    result = {input_path: output_path for input_path, output_path in zip(input_paths, output_paths)}
    return result


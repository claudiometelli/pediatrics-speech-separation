from config import ROOT_DIR, MAIN_INPUT_DIR, TEXT_DIR
patients_text_path = ROOT_DIR + MAIN_INPUT_DIR + TEXT_DIR + "/patients.txt"
patient_text_path = ROOT_DIR + MAIN_INPUT_DIR + TEXT_DIR + "/patient.txt"


def get_patient() -> str:
    f = open(patient_text_path)
    patient = f.readline().replace("\n", "")
    return patient


def get_patients() -> list:
    f = open(patients_text_path)
    lines = f.readlines()
    patients = [line.replace("\n", "") for line in lines]
    return patients

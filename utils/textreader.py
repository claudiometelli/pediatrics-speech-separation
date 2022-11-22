patients_text_path = "../assets/text/patients.txt"
patient_text_path = "../assets/text/patient.txt"


def get_patient() -> str:
    f = open(patient_text_path)
    patient = f.readline()
    return patient


def get_patients() -> list:
    f = open(patients_text_path)
    lines = f.readlines()
    patients = [line.replace("\n", "") for line in lines]
    return patients

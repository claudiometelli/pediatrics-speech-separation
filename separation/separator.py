import torchaudio
from speechbrain.pretrained import SepformerSeparation as separator
from config import SEPFORMER_OUTPUT_DIR, SEPARATOR_ALL, SEPARATOR_IDS
from utils.ioutils import get_patients_name, get_patient_name_by_id, get_patients_audio_path, \
    get_patient_audio_path_by_id, get_patients_output_directory_path, get_patient_output_directory_path_by_id


if __name__ == "__main__":
    # Get patients name and path from config
    patients = {}
    if SEPARATOR_ALL:
        patient_paths = zip(get_patients_name(), get_patients_audio_path(), get_patients_output_directory_path())
    else:
        names = [get_patient_name_by_id(patient_id) for patient_id in SEPARATOR_IDS]
        input_paths = [get_patient_audio_path_by_id(patient_id) for patient_id in SEPARATOR_IDS]
        output_paths = [get_patient_output_directory_path_by_id(patient_id) for patient_id in SEPARATOR_IDS]
        patient_paths = zip(names, input_paths, output_paths)

    # Set input file and output file for each patient
    patients = {patient: {
        "input": f"{input_path}",
        "output_p1": f"{output_path}{SEPFORMER_OUTPUT_DIR}{patient}_p1.wav",
        "output_p2": f"{output_path}{SEPFORMER_OUTPUT_DIR}{patient}_p2.wav"
    } for patient, input_path, output_path in patient_paths}

    # Applying SepFormer model
    for patient, paths in patients.items():
        # Separating files
        model = separator.from_hparams(source="speechbrain/sepformer-whamr", savedir="pretrained_models/sepformer-whamr")
        est_sources = model.separate_file(paths.get("input"))
        # Write output
        torchaudio.save(paths.get("output_p1"), est_sources[:, :, 0].detach().cpu(), 8000)
        torchaudio.save(paths.get("output_p2"), est_sources[:, :, 1].detach().cpu(), 8000)

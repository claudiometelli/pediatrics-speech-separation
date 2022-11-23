import torchaudio
from speechbrain.pretrained import SepformerSeparation as separator
from config import ROOT_DIR, MAIN_INPUT_DIR, AUDIO_DIR, PATIENTS_DIR, MAIN_OUTPUT_DIR, MASTER_OUTPUT_DIR
from utils.textreader import get_patient

# Get patient name and personal directory
patient = get_patient()
patient_directory = patient.replace(" ", "_") + "/"

input_file = patient + ".wav"
input_path = ROOT_DIR + MAIN_INPUT_DIR + AUDIO_DIR + PATIENTS_DIR + patient_directory + input_file

general_output_file_name = patient.replace(" ", "_")
output_file_signature_1 = "_p1.wav"
output_file_signature_2 = "_p2.wav"
output_dir = ROOT_DIR + MAIN_OUTPUT_DIR + AUDIO_DIR + PATIENTS_DIR + patient_directory + MASTER_OUTPUT_DIR

# Separating files
model = separator.from_hparams(source="speechbrain/sepformer-whamr", savedir="pretrained_models/sepformer-whamr")
est_sources = model.separate_file(input_path)

# Write output
torchaudio.save(
    output_dir + general_output_file_name + output_file_signature_1, est_sources[:, :, 0].detach().cpu(), 8000
    )
torchaudio.save(
    output_dir + general_output_file_name + output_file_signature_2, est_sources[:, :, 1].detach().cpu(), 8000
    )

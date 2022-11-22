import torchaudio
from speechbrain.pretrained import SepformerSeparation as separator
from utils.configreader import main_input_directory, patients_directory, split_audio_directory, main_output_directory, \
    master_output_directory
from utils.textreader import get_patient

# Data to be split and directory names
patient = get_patient()

patient_directory = patient.replace(" ", "_") + "/"
input_file = patient + ".wav"
input_path = "../" + main_input_directory + patients_directory + patient_directory + input_file

general_output_file_name = patient.replace(" ", "_")
output_file_signature_1 = "_p1.wav"
output_file_signature_2 = "_p2.wav"
output_path = "../" + main_output_directory + patients_directory + patient_directory + master_output_directory + general_output_file_name

# Separating files
model = separator.from_hparams(source="speechbrain/sepformer-whamr", savedir="pretrained_models/sepformer-whamr")
est_sources = model.separate_file(input_path)

# Write output
torchaudio.save(output_path + output_file_signature_1, est_sources[:, :, 0].detach().cpu(), 8000)
torchaudio.save(output_path + output_file_signature_2, est_sources[:, :, 1].detach().cpu(), 8000)

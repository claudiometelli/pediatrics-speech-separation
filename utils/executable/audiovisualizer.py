import os
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

from beans.PatientAudio import PatientAudio
from config import ROOT_DIR, MAIN_INPUT_DIR, AUDIO_DIR, PATIENTS_DIR, SPECTRUM_DIR, WAVEFORM_DIR, SHOW_WAVEFORM, \
    SHOW_SPECTRUM, SHOW_MELSPECTROGRAM
from utils.textreader import get_patient


# Set plot on an waveform plot
def set_waveform_plot(audio: PatientAudio):
    plt.plot(
        np.linspace(
            1, audio.get_audio().shape[0], audio.get_audio().shape[0]
        ) / audio.get_samplerate(), audio.get_audio()
    )
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")


# Set plot on a full time spectrum plot
def set_spectrum_plot(audio: PatientAudio):
    plt.figure(figsize=(12, 8))
    librosa.display.specshow(
        librosa.amplitude_to_db(audio.get_spectrum()[:], ref=np.max),
        x_axis="time",
        y_axis="log",
        sr=audio.get_samplerate()
        )
    plt.title("Full Spectrum")
    plt.colorbar()


# Set plot on a mel-spectrogram plot
def set_melspectrogram_plot(audio: PatientAudio):
    plt.figure(figsize=(12, 8))
    librosa.display.specshow(
        librosa.amplitude_to_db(np.abs(audio.get_melspectrogram())[:], ref=np.max),
        x_axis="time",
        y_axis="log",
        sr=audio.get_samplerate()
    )
    plt.title("Mel Spectrogram")
    plt.colorbar()


# Save plot on a specific data path and clear the plot
def save_plot(data_path: str):
    plt.savefig(data_path)
    plt.clf()


"""
This dictionary contains all plot types
For every type of plot there is:
    - "directory": the directory name where plot will be saved
    - "show": a boolean variable read from the config file which indicates what plot must be saved
    - "func": the function to set te plot
"""
plots = {
    "waveform": {
        "directory": WAVEFORM_DIR,
        "show": SHOW_WAVEFORM,
        "func": set_waveform_plot,
        "file_signature": "waveform"
    },
    "spectrogram": {
        "directory": SPECTRUM_DIR,
        "show": SHOW_SPECTRUM,
        "func": set_spectrum_plot,
        "file_signature": "spectrum"
    },
    "melspectrogram": {
        "directory": SPECTRUM_DIR,
        "show": SHOW_MELSPECTROGRAM,
        "func": set_melspectrogram_plot,
        "file_signature": "mel_spectrogram"
    }
}

if __name__ == "__main__":
    # Get patient name
    patient = get_patient()
    patient_directory = patient.replace(" ", "_") + "/"

    # Set input directories
    input_file_name = patient + ".wav"
    input_path = ROOT_DIR + MAIN_INPUT_DIR + AUDIO_DIR + PATIENTS_DIR + patient_directory + input_file_name
    input_audio = PatientAudio(input_path)

    # Read the plots dictionary and save plot if specified
    for plot in plots.keys():
        # If plot must be saved
        if plots[plot].get("show"):
            # Set output directories and create if doesn't exist
            output_dir = ROOT_DIR + MAIN_INPUT_DIR + AUDIO_DIR + PATIENTS_DIR + patient_directory + plots[plot].get(
                "directory"
                )
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            output_file_path = output_dir + patient.replace(" ", "_") + "_" + plots[plot].get("file_signature") + ".png"
            # Execute function for plotting
            plots[plot].get("func")(input_audio)
            # Save plot
            save_plot(output_file_path)

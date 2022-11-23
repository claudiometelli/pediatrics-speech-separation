import os
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

from beans.PatientAudio import PatientAudio
from config import ROOT_DIR, MAIN_INPUT_DIR, AUDIO_DIR, PATIENTS_DIR, SPECTRUM_DIR, TIME_SERIES_DIR, SHOW_TIME_SERIES, \
    SHOW_FULL_SPECTRUM
from utils.textreader import get_patient


def set_time_series_plot(audio: PatientAudio):
    plt.plot(
        np.linspace(
            1, audio.get_audio().shape[0], audio.get_audio().shape[0]
        ) / audio.get_samplerate(), audio.get_audio()
    )
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")


def set_full_spectrum_plot(audio: PatientAudio):
    audio.get_full_spectrum()
    plt.figure(figsize=(12, 8))
    librosa.display.specshow(
        librosa.amplitude_to_db(audio.get_full_spectrum()[:], ref=np.max),
        x_axis="time",
        y_axis="log",
        sr=audio.get_samplerate()
        )
    plt.title("Full spectrum")
    plt.colorbar()


def save_plot(data_path: str):
    plt.savefig(data_path)
    plt.clf()


plots = {
    "time_series": {
        "directory": TIME_SERIES_DIR,
        "show": SHOW_TIME_SERIES,
        "func": set_time_series_plot
    },
    "full_spectrum": {
        "directory": SPECTRUM_DIR,
        "show": SHOW_FULL_SPECTRUM,
        "func": set_full_spectrum_plot
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

    for plot in plots.keys():
        if plots[plot].get("show"):
            # Set output directories and create if doesn't exist
            output_dir = ROOT_DIR + MAIN_INPUT_DIR + AUDIO_DIR + PATIENTS_DIR + patient_directory + plots[plot].get(
                "directory"
                )
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            output_file_path = output_dir + input_file_name.replace(".wav", ".png")
            # Execute function for plotting
            plots[plot].get("func")(input_audio)
            # Save plot
            save_plot(output_file_path)

import librosa

import utils.audioutils as audioutils


class PatientAudio:

    def __init__(self, data_path: str):
        raw_audio = audioutils.load_audio(data_path)
        self.__audio = raw_audio.get_audio()
        self.__samplerate = raw_audio.get_samplerate()

    def get_audio(self):
        return self.__audio

    def get_samplerate(self):
        return self.__samplerate

    def get_full_spectrum_and_phase(self):
        s = librosa.stft(self.__audio)
        s_full, phase = librosa.magphase(s)
        return s_full, phase

    def get_full_spectrum(self):
        s = librosa.stft(self.__audio)
        s_full, phase = librosa.magphase(s)
        return s_full

    def get_phase(self):
        s = librosa.stft(self.__audio)
        s_full, phase = librosa.magphase(s)
        return phase

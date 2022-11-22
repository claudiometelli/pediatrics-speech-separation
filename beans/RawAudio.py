import os
import librosa
import numpy as np


class RawAudio:

    # Hope python will implement multi __init__ one day...
    def __init__(self):
        self.__data_path = None
        self.__audio = None
        self.__samplerate = None
        self.__offset = None
        self.__audio_duration = None

    def load_audio(self, data_path: str, samplerate: int, offset: float, audio_duration: None or float) -> None:
        assert os.path.exists(data_path), "File at: " + str(data_path) + " not found"
        self.__data_path = data_path
        self.__offset = offset
        self.__audio_duration = audio_duration
        self.__audio, self.__samplerate = librosa.load(
            data_path, sr=samplerate, offset=self.__offset, duration=self.__audio_duration
            )

    def assemble_audio(self, audio: np.ndarray, samplerate: int, offset: float, audio_duration: None or float):
        # TODO add asserts
        self.__audio = audio
        if offset > 0.0:
            self.add_offset(offset)
        if audio_duration is not None:
            self.add_duration(audio_duration)
        self.__samplerate = samplerate
        self.__offset = offset
        self.__audio_duration = librosa.get_duration(y=self.__audio, sr=self.__samplerate)

    def add_offset(self, offset: float):
        starting_point = round(self.__samplerate * offset)
        self.__audio = self.__audio[starting_point:]

    def add_duration(self, audio_duration: float):
        duration_points = round(self.__samplerate * audio_duration)
        self.__audio = self.__audio_duration[:duration_points]

    def get_data_path(self) -> str:
        return self.__data_path

    def get_audio(self) -> np.ndarray:
        return self.__audio

    def get_samplerate(self) -> int:
        return self.__samplerate

    def get_offset(self) -> float:
        return self.__offset

    def get_audio_duration(self) -> float:
        return self.__audio_duration

    def __str__(self):
        result = "Audio Path: "
        result += self.__data_path if self.__data_path is not None else "None"
        result += "\nAudio Samplerate: "
        result += str(self.__samplerate) if self.__samplerate is not None else "None"
        result += "\nAudio Offset: "
        result += str(self.__offset) if self.__offset is not None else "None"
        result += "\nAudio Duration: "
        result += str(self.__audio_duration) if self.__audio_duration is not None else "None"
        result += "\nAudio Shape: "
        result += str(self.__audio.shape) if self.__audio is not None else "None"
        return result

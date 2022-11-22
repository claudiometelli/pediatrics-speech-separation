import numpy as np
import soundfile as sf
from beans.RawAudio import RawAudio

from configreader import default_audio_samplerate, default_audio_offset, default_audio_duration


def load_audio(data_path: str, samplerate=default_audio_samplerate, offset=default_audio_offset,
               audio_duration=default_audio_duration) -> RawAudio:
    result = RawAudio()
    result.load_audio(data_path, samplerate, offset, audio_duration)
    return result


def write_audio(data_path: str, audio: RawAudio) -> None:
    # TODO check if data_path exists
    sf.write(data_path, audio.get_audio(), audio.get_samplerate())


def add_audio(audio_1: RawAudio, audio_2: RawAudio) -> RawAudio:
    assert isinstance(audio_1, RawAudio), "Audio must be a RawAudio Object"
    assert isinstance(audio_2, RawAudio), "Audio must be a RawAudio Object"
    assert audio_1.get_samplerate() == audio_2.get_samplerate(), "The two audio must have the same samplerate"
    result = RawAudio()
    result.assemble_audio(
        np.concatenate((audio_1.get_audio(), audio_2.get_audio())), audio_1.get_samplerate(), default_audio_offset,
        default_audio_duration
        )
    return result

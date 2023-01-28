import numpy as np
import soundfile as sf
from pyannote.audio import Pipeline
from utils.logger import diarization_log
from utils.ioutils import get_input_output_diarization_paths


@diarization_log
def diarization(file, speakers=None):
    print("Starting Diarization")
    # Get diarization model
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization@2.1", use_auth_token="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"
    )
    sp_diarization = pipeline(file) if speakers is not None else pipeline(file, num_speakers=speakers)
    return sp_diarization


def main():
    for input_file, output_file in get_input_output_diarization_paths().items():
        original_audio, samplerate = sf.read(input_file)
        sp_diarization = diarization(input_file)
        diarization_map = {}
        # Create dictionary to process output data
        for turn, turn_id, speaker in sp_diarization.itertracks(yield_label=True):
            if diarization_map.get(speaker) is None:
                diarization_map[speaker] = [(turn.start, turn.end)]
            else:
                diarization_map.get(speaker).append((turn.start, turn.end))
        # Create output audio
        for speaker in diarization_map:
            res = np.zeros(samplerate)
            for segment in diarization_map.get(speaker):
                start_index = int(segment[0] * samplerate)
                last_index = int(segment[1] * samplerate)
                print(start_index, last_index)
                res = np.concatenate((res, original_audio[start_index:last_index], np.zeros(samplerate)))
            sf.write(output_file + speaker.wav, res, samplerate)


if __name__=="__main__":
    main()

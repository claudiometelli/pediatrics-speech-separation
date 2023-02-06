import numpy as np
import soundfile as sf
from pyannote.audio import Pipeline
from config import DIARIZATION_OUTPUT_DIR, DIARIZATION_ALL, DIARIZATION_IDS, DIARIZATION_MODEL_OUTPUT_ORIGINAL, \
    DIARIZATION_MODEL_OUTPUT_SIZING
from utils.logger import diarization_log
from utils.ioutils import get_patients_name, get_patient_name_by_id, get_patients_audio_path, \
    get_patient_audio_path_by_id, get_patients_output_directory_path, get_patient_output_directory_path_by_id, get_token


@diarization_log
def diarization(file, speakers=None):
    print("Starting Diarization")
    # Get diarization model
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization@2.1", use_auth_token=get_token()
    )
    sp_diarization = pipeline(file) if speakers is None else pipeline(file, num_speakers=speakers)
    return sp_diarization


def main():
    # Get patients name and path from config
    if DIARIZATION_ALL:
        patient_paths = zip(get_patients_name(), get_patients_audio_path(), get_patients_output_directory_path())
    else:
        names = [get_patient_name_by_id(patient_id) for patient_id in DIARIZATION_IDS]
        input_paths = [get_patient_audio_path_by_id(patient_id) for patient_id in DIARIZATION_IDS]
        output_paths = [get_patient_output_directory_path_by_id(patient_id) for patient_id in DIARIZATION_IDS]
        patient_paths = zip(names, input_paths, output_paths)
    # Set patient input and output
    patients = {patient: {
        "input": f"{input_path}",
        "output": f"{output_path}{DIARIZATION_OUTPUT_DIR}{patient}_SPEAKER.wav",
    } for patient, input_path, output_path in patient_paths}
    # Create output
    for patient, paths in patients.items():
        input_file = paths.get("input")
        original_audio, samplerate = sf.read(input_file)
        sp_diarization = diarization(input_file, speakers=2)
        diarization_map = {}
        # Create dictionary to process output data
        for turn, turn_id, speaker in sp_diarization.itertracks(yield_label=True):
            if diarization_map.get(speaker) is None:
                diarization_map[speaker] = [(turn.start, turn.end)]
            else:
                diarization_map.get(speaker).append((turn.start, turn.end))
        # Create output audio
        # Write on the original length the output audio
        if DIARIZATION_MODEL_OUTPUT_ORIGINAL:
            for speaker in diarization_map:
                result = np.zeros(original_audio.shape)
                for segment in diarization_map.get(speaker):
                    start_index = int(segment[0] * samplerate)
                    last_index = int(segment[1] * samplerate)
                    # Write result for each audio channel
                    for channel in range(original_audio.shape[1]):
                        result[start_index:last_index, channel] = original_audio[start_index:last_index, channel]
                # Write audio on file system
                sf.write(paths.get("output").replace("SPEAKER", speaker), result, samplerate)
        else:
            space_between_segments = DIARIZATION_MODEL_OUTPUT_SIZING * samplerate
            for speaker in diarization_map:
                # Get final audio dimension
                final_dimension = 0
                for segment in diarization_map.get(speaker):
                    start_index = int(segment[0] * samplerate)
                    last_index = int(segment[1] * samplerate)
                    final_dimension += (last_index - start_index)
                final_dimension += space_between_segments * (len(diarization_map.get(speaker)) + 1)

                result = np.zeros((final_dimension, original_audio.shape[1]))
                # Use this variable to identify next index where starting writing output data
                next_index = space_between_segments
                for segment in diarization_map.get(speaker):
                    start_index = int(segment[0] * samplerate)
                    last_index = int(segment[1] * samplerate)
                    # Write result for each audio channel
                    for channel in range(original_audio.shape[1]):
                        result[next_index:next_index+(last_index-start_index), channel] = original_audio[start_index:last_index, channel]
                    next_index = next_index+(last_index-start_index) + space_between_segments
                # Write audio on file system
                sf.write(paths.get("output").replace("SPEAKER", speaker), result, samplerate)


if __name__ == "__main__":
    main()

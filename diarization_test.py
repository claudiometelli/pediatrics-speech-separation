import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from config import ROOT_DIR, MAIN_OUTPUT_DIR, TEXT_DIR, AUDIO_DIR, PATIENTS_DIR
from utils.ioutils import get_patient_name_by_id, get_patient_directory_path_by_id, get_patient_audio_path_by_id


def get_results_from_test(patient_id: int) -> dict:
    """
    returns test results from test.txt
    :param patient_id: the id of the patient
    :return: a dict where the key is the speaker id and the value is a list of tuples
        with start and end for every segment of the speaker
    """
    result = {"general_data": get_patient_audio_path_by_id(patient_id), "speakers": {}}
    with open(f"{get_patient_directory_path_by_id(patient_id)}test.txt") as f:
        lines = f.readlines()
        # Read lines where segmentation of single speaker starts and sort
        speakers_start = [line_index for line_index in range(len(lines)) if lines[line_index].startswith("SPEAKER")]
        speakers_start.sort()
        # Read lines for all speaker from where begin to the end of the speaker segments
        for speaker_index in range(len(speakers_start)):
            # Index of the line where the speaker starts
            speaker_start = speakers_start[speaker_index]
            # Index of the line where the speaker ends
            speaker_end = speakers_start[speaker_index + 1] - 1 if speaker_index < len(speakers_start) - 1 else len(lines) - 1
            # Speaker name extracted from the line (es. SPEAKER_01)
            speaker_name = lines[speaker_start][:10]
            result.get("speakers")[speaker_name] = []
            for line_index in range(speaker_start, speaker_end + 1):
                current_line = lines[line_index].replace("\n", "")
                # Generic controls (current line must be like like "1.01-2.02")
                if current_line.startswith("SPEAKER") or current_line == "":
                    continue
                if current_line.count("-") != 1 or current_line.count(".") != 2:
                    continue
                if not current_line.replace("-", "").replace(".", "").isdigit():
                    continue
                separator_index = current_line.index("-")
                segment_start = float(current_line[:separator_index])
                segment_end = float(current_line[separator_index + 1:])
                result.get("speakers")[speaker_name].append((segment_start, segment_end))
    return result


def get_results_from_log(patient_id: int) -> dict:
    """
    returns log results from diarization_log.txt for a single patient
    :param patient_id: the id of the patient
    :return: a dict where the key is the speaker id and the value is a list of tuples
        with start and end for every segment of the speaker
    """
    def convert_line(line: str) -> tuple:
        # Convert a single line in tuple with format: (speaker, segment_start, segment_end)
        res = line.replace("\n", "").replace(" ", "").replace("=", "")
        res = res.replace("start", "").replace("stop", "").replace("min", "").replace("sec", "").replace("sp", "")
        comma_1_index = res.index(",")
        comma_2_index = comma_1_index + 1 + res[comma_1_index+1:].index(",")
        comma_3_index = comma_2_index + 1 + res[comma_2_index+1:].index(",")
        comma_4_index = comma_3_index + 1 + res[comma_3_index+1:].index(",")
        start_minutes = int(res[:comma_1_index])
        start_seconds = float(res[comma_1_index+1:comma_2_index])
        end_minutes = int(res[comma_2_index+1:comma_3_index])
        end_seconds = float(res[comma_3_index+1:comma_4_index])
        speaker_name = res[comma_4_index+1:]
        return speaker_name, start_minutes * 60 + start_seconds, end_minutes * 60 + end_seconds

    result = {"general_data": get_patient_audio_path_by_id(patient_id), "speakers": {}}
    patient = get_patient_name_by_id(patient_id)
    with open(ROOT_DIR + MAIN_OUTPUT_DIR + TEXT_DIR + "diarization_log.txt") as f:
        lines = f.readlines()
        # Get starting line index for the patient in log file (es."file: Mario Rossi.wav, execution time: 3 min, 33.5 sec")
        start_index = next(line_index for line_index in range(len(lines)) if lines[line_index].count(patient) == 1)
        # Get ending line for the patient in log file (es."--End--")
        end_index = start_index + lines[start_index:].index("--End--\n")
        # Get speakers
        speakers = set([line[len(line)-11:].replace("\n", "") for line in lines[start_index+1:end_index]])
        for speaker in speakers:
            result.get("speakers")[speaker] = []
        for line in lines[start_index+1:end_index+1]:
            if line.count(",") != 4:
                continue
            speaker, segment_start, segment_end = convert_line(line)
            result.get("speakers")[speaker].append((segment_start, segment_end))
    return result


def get_vad_result(diarization_test: dict, result_test: dict):
    assert diarization_test.get("general_data") == result_test.get("general_data")
    audio_data, samplerate = sf.read(diarization_test.get("general_data"))
    total_test_length = int((audio_data.shape[0] / samplerate) * 100)
    diarization_data = np.zeros(total_test_length)
    result_data = np.zeros(total_test_length)
    diarization_segments = []
    result_segments = []
    for segments in diarization_test.get("speakers").values():
        diarization_segments.extend(segments)
    for segments in result_test.get("speakers").values():
        result_segments.extend(segments)
    for segment in diarization_segments:
        segment_start_cent = int(segment[0] * 100)
        segment_end_cent = int(segment[1] * 100)
        diarization_data[segment_start_cent:segment_end_cent] = 1
    for segment in result_segments:
        segment_start_cent = int(segment[0] * 100)
        segment_end_cent = int(segment[1] * 100)
        result_data[segment_start_cent:segment_end_cent] = 1
    overlapped_1s = np.logical_and(diarization_data, result_data)
    overlapped_0s = np.logical_or(diarization_data, result_data)
    overlapped_0s_and_1s = np.logical_not(np.logical_xor(diarization_data, result_data))
    missed_1s = np.logical_xor(overlapped_1s, result_data)
    missed_0s = np.logical_xor(overlapped_0s, result_data)
    total_accuracy = np.count_nonzero(overlapped_0s_and_1s) / total_test_length
    accuracy_1s = np.count_nonzero(overlapped_1s) / np.count_nonzero(result_data)
    accuracy_0s = np.count_nonzero(missed_0s) / (total_test_length - np.count_nonzero(result_data))
    plt.figure(figsize=(20, 10))
    print(f"Total VAD accuracy: {total_accuracy}",
          f"Accuracy on speaking segments: {accuracy_1s}",
          f"Wrong detecting: {accuracy_0s}",
          sep="\n")
    # plt.plot(np.arange(0, total_test_length / 100, 0.01), diarization_data, label="diarization data")
    plt.plot(np.arange(0, total_test_length / 100, 0.01), result_data, label="result data")
    plt.plot(np.arange(0, total_test_length / 100, 0.01), overlapped_1s, label="overlapped data")
    plt.savefig(ROOT_DIR + MAIN_OUTPUT_DIR + AUDIO_DIR + PATIENTS_DIR + f"Fattori_Matilde/vad_plot_over.png")
    plt.legend()
    plt.show()


def get_speaker_accuracy(diarization_test: dict, result_test: dict):
    assert diarization_test.get("general_data") == result_test.get("general_data")
    assert len(diarization_test.get("speakers")) == len(result_test.get("speakers"))
    audio_data, samplerate = sf.read(diarization_test.get("general_data"))
    total_test_length = int((audio_data.shape[0] / samplerate) * 100)
    for speaker, result_segments in result_test.get("speakers").items():
        diarization_segments = diarization_test.get("speakers").get(speaker)
        diarization_data = np.zeros(total_test_length)
        result_data = np.zeros(total_test_length)
        for segment in diarization_segments:
            segment_start_cent = int(segment[0] * 100)
            segment_end_cent = int(segment[1] * 100)
            diarization_data[segment_start_cent:segment_end_cent] = 1
        for segment in result_segments:
            segment_start_cent = int(segment[0] * 100)
            segment_end_cent = int(segment[1] * 100)
            result_data[segment_start_cent:segment_end_cent] = 1
        overlapped_1s = np.logical_and(diarization_data, result_data)
        overlapped_0s = np.logical_or(diarization_data, result_data)
        overlapped_0s_and_1s = np.logical_not(np.logical_xor(diarization_data, result_data))
        missed_1s = np.logical_xor(overlapped_1s, result_data)
        overused_1s = np.logical_xor(overlapped_1s, diarization_data)
        total_accuracy = np.count_nonzero(overlapped_0s_and_1s) / total_test_length
        accuracy_1s = np.count_nonzero(overlapped_1s) / np.count_nonzero(result_data)
        wrong_1s = np.count_nonzero(overlapped_1s) / (total_test_length - np.count_nonzero(result_data))
        print(f"Speaker:{speaker}",
              f"Total Speaker accuracy: {total_accuracy}",
              f"Accuracy on talking segments: {accuracy_1s}",
              f"Wrong detection accuracy : {wrong_1s}",
              sep="\n")
        plt.figure(figsize=(20, 10))
        plt.title(speaker)
        plt.plot(np.arange(0, total_test_length / 100, 0.01), diarization_data, label="diarization data")
        plt.plot(np.arange(0, total_test_length / 100, 0.01), result_data, label="result data")
        # plt.plot(np.arange(0, total_test_length / 100, 0.01), overlapped_1s, label="overlapped data")
        plt.savefig(ROOT_DIR + MAIN_OUTPUT_DIR + AUDIO_DIR + PATIENTS_DIR + f"Fattori_Matilde/plot_over_{speaker}.png")
        plt.legend()
        plt.show()


log_res = get_results_from_log(6)
test_res = get_results_from_test(6)
# get_vad_result(log_res, test_res)
get_speaker_accuracy(log_res, test_res)

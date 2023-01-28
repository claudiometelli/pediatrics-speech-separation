import time
from config import ROOT_DIR, MAIN_OUTPUT_DIR, TEXT_DIR


def diarization_log(func):

    log_file = ROOT_DIR + MAIN_OUTPUT_DIR + TEXT_DIR + "diarization_log.txt"

    def second_to_string(sec: float) -> str:
        return f"{int(sec / 60)} min, {round(sec % 60, 2)} sec"

    def wrapper(*args, **kwargs):
        before_time = time.time()
        sp_diarization = func(*args, **kwargs)
        after_time = time.time()
        with open(log_file, "a") as f:
            f.write(
                f"file: {args[0]},"
                f"execution time: {second_to_string(after_time - before_time)} sec,"
                f"init_speakers={kwargs['speakers']}\n"
                )
            for turn, _, speaker in sp_diarization.itertracks(yield_label=True):
                res = f"start = {second_to_string(turn.start)}, stop = {second_to_string(turn.end)}, sp = {speaker}"
                print(res)
                f.write(res + "\n")
            f.write("--End--\n")
    return wrapper

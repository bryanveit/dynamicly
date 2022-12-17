import soundfile as sf
import sounddevice as sd
from dynamicly.signal.sample_rate import calc_sample_rate
from dynamicly.misc.math import normalize


def play_audio(time_history, loop=False, norm=False):
    fs = int(calc_sample_rate(time_history))
    if norm:
        time_history = normalize(time_history)
    sd.play(time_history[:, -1], fs, loop=loop)
    return

import soundfile as sf
import sounddevice as sd
from dynamicly.signal.sample_rate import calc_sample_rate

def play_audio(data, loop = False):
    fs = int(calc_sample_rate(data))
    sd.play(data[:,-1],fs,loop=loop)
    return


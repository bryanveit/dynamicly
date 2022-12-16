import numpy as np

def sine_wave(freq=1, length=1, dt=0.001, magnitude=1):
    T = 1 / freq

    time = np.arange(0, length + dt, dt)
    w = freq * 2 * np.pi
    y = np.sin(w * time)
    y *= magnitude
    return np.column_stack([time, y])

def sine_sweep(freq1=10, freq2=2000, length=1, dt=0.001, magnitude=1):
    pass

def half_sine_pulse(pulse_width=0.005, magnitude=10, length=None, fs=10000):
    T = 2 * pulse_width
    f = 1 / T
    if length is None:
        length = pulse_width * 100
    time = np.arange(0, length, 1 / fs)
    w = f * 2 * np.pi
    y = np.sin(w * time)
    y[np.where(time > pulse_width)] = 0
    y *= magnitude

    return np.column_stack([time, y])

import numpy as np

def sine_wave(freq=1, length=1, dt=0.001, magnitude=1):
    T = 1 / freq

    time = np.arange(0, length + dt, dt)
    w = freq * 2 * np.pi
    y = np.sin(w * time)
    y *= magnitude
    return np.column_stack([time, y])

def sine_sweep(freq1=10, freq2=2000, length=1, dt=0.001, magnitude=1, type='linear'):
    time = np.arange(0, length + dt, dt)
    n = len(time)
    period = length

    if type == 'linear':
        y = magnitude*np.sin(2*np.pi*(freq1*time + ((freq2-freq1)*time**2)/(2*period)))
    elif type == 'log' or type == 'logarithmic':
        y = magnitude*np.sin(2*np.pi*freq1*period*(((freq2/freq1)**(time/period)-1)/np.log(freq2/freq1)))
    else:
        print('unsupported type.')
        return

    return np.column_stack([time,y])

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

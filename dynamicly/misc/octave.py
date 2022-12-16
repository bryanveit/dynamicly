import numpy as np
from dynamicly.misc.interpolation import log_log_interp, linear_interp

def octave(f1=20, f2=2000, n=1 / 6, standard=False, ansi=False):
    if ansi:
        freq = [
            20,
            25,
            31.5,
            40,
            50,
            63,
            80,
            100,
            125,
            160,
            200,
            250,
            315,
            400,
            500,
            630,
            800,
            1000,
            1250,
            1600,
            2000,
            2500,
            3150,
            4000,
            5000,
            6300,
            8000,
            10000
        ]
    elif standard:
        freq = [
            20,
            22.36,
            25,
            28.06,
            31.5,
            35.5,
            40,
            44.72,
            50,
            56.12,
            63,
            70.99,
            80,
            89.44,
            100,
            111.8,
            125,
            141.42,
            160,
            178.89,
            200,
            223.61,
            250,
            280.62,
            315,
            354.96,
            400,
            447.21,
            500,
            561.25,
            630,
            709.93,
            800,
            894.43,
            1000,
            1118.03,
            1250,
            1414.21,
            1600,
            1788.85,
            2000
        ]
    else:
        # 10 * 2 ** (n / 6)
        freq = []
        i = 0
        while True:
            f = f1 * 2 ** (i * n)
            freq.append(f)
            if f >= f2:
                break
            i += 1

    freq = np.asarray(freq)
    return freq

def narrow(f1=20, f2=2000, df=1):
    # perhaps narrow isnt the best name but for constant frequency spacing,
    # often will be for narrow band 1 hz etc spacing
    # this implementation should allow natural spacing to go beyond f2 but
    # could also use np.arange or something
    freq = [f1]
    i = 0
    f = f1
    while True:
        f += df
        freq.append(f)
        if f >= f2:
            break
        i += 1
    freq = np.asarray(freq)
    return freq

def to_sixth_octave(some_array, f1=20, f2=2000, standard=False, ansi=False):
    # THIS IS PURE INTERPOLATION BAND AVERAGING IS NOT IMPLEMENTED
    oct_freq = octave(f1=f1, f2=f2, n=1 / 6, standard=standard, ansi=ansi)
    new_array = log_log_interp(some_array[:, 0], some_array[:, -1], oct_freq)
    return new_array

def to_third_octave(some_array, f1=20, f2=10000, ansi=True):
    oct_freq = octave(f1=f1, f2=f2, n=1 / 3, standard=False, ansi=ansi)
    new_array = log_log_interp(some_array[:, 0], some_array[:, -1], oct_freq)
    return new_array

def to_narrow(some_array, f1=20, f2=2000, df=1, log=True):
    nar_freq = narrow(f1=f1, f2=f2, df=df)
    if log:
        new_array = log_log_interp(some_array[:, 0], some_array[:, -1],
                                   nar_freq)
    else:
        new_array = linear_interp(some_array[:, 0], some_array[:, -1], nar_freq)
    return new_array

# This uses a method of band averaging
def to_sixth_band_averaging(narrow_data, octave=1 / 6, f1=None, f2=None):
    frequency = narrow_data[:, 0]
    magnitude = narrow_data[:, -1]
    if f1 is None:
        f1 = 20
    if f2 is None:
        f2 = 2000
    n = len(narrow_data)

    # this could use the functions created already but going to stick close
    # to the matlab method for now (not using standard frequency band center
    # frequencies.... are those ANSI? or just an industry thing?
    number_of_octaves = np.log2(f2 / f1)
    i = np.arange(0, np.floor(number_of_octaves / octave) + 1, 1)

    center_freqs = f1 * 2 ** (i * octave)
    if center_freqs[-1] < f2:
        center_freqs = np.append(center_freqs, f2)

    n_bands = len(center_freqs)

    low_freqs = center_freqs * 2 ** (-octave / 2)
    hi_freqs = center_freqs * 2 ** (octave / 2)

    low_freqs[n_bands - 1] = hi_freqs[n_bands - 2]
    hi_freqs[n_bands - 1] = center_freqs[n_bands - 1]

    if frequency[0] == 0:
        frequency = frequency[1:]
        magnitude = magnitude[1:]
        n -= 1

    df = np.mean(np.diff(frequency))
    df_half = df / 2 * (0.999999)  # non inclusive
    three_freqs = np.asarray([frequency - df_half,
                              frequency,
                              frequency + df_half]).T
    three_freqs = np.reshape(three_freqs, n * 3)
    three_mags = np.asarray([magnitude,
                             magnitude,
                             magnitude]).T
    three_mags = np.reshape(three_mags, n * 3)

    new_freq = np.arange(np.min(three_freqs), np.max(three_freqs), df / 10)
    new_mag = log_log_interp(three_freqs, three_mags, new_freq)[:, -1]
    new_df = np.mean(np.diff(new_freq))

    octave_freq = center_freqs
    octave_mag = []
    for low, high in zip(low_freqs, hi_freqs):
        # indices = np.where(new_freq >= low) and np.where(new_freq <= high)
        indices = np.where((new_freq >= low) & (new_freq <= high))
        if len(indices[0]) == 0:
            continue
        applicalbe_mags = new_mag[indices]
        band_average = (np.sum(applicalbe_mags) * new_df) / (high - low)
        octave_mag.append(band_average)
    octave_mag = np.asarray(octave_mag)

    if len(octave_mag) != len(octave_freq):
        try:
            if len(octave_freq) > len(octave_mag):
                octave_freq = octave_freq[:-1]
            else:
                octave_mag = octave_mag[:-1]
            octave_data = np.column_stack([octave_freq,
                                           octave_mag])
        except:
            print('something wrong with the frequency bounds / not programmed to '
                  'handle it yet')
            return None
        # octave_freq = octave_freq[: -1]
    octave_data = np.column_stack([octave_freq,
                                   octave_mag])
    return octave_data
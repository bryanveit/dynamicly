import numpy as np
from dynamicly.misc.octave import to_narrow, narrow, octave
from dynamicly.misc.interpolation import log_log_interp


def power_to_dB(data):
    if isinstance(data, dict):
        new_data = {}
        for key, data_i in data.items():
            freq_i = data_i[:, 0]
            db_data_i = 10 * np.log10(data_i[:, -1])
            new_data[key] = np.column_stack([freq_i,
                                             db_data_i])
        return new_data
    elif isinstance(data, np.ndarray):
        freq = data[:, 0]
        db_data = 10 * np.log10(data[:, -1])
        new_data = np.column_stack([freq,
                                    db_data])
        return new_data
    else:
        return None


def amplitude_to_dB(data):
    if isinstance(data, dict):
        new_data = {}
        for key, data_i in data.items():
            freq_i = data_i[:, 0]
            db_data_i = 20 * np.log10(data_i[:, -1])
            new_data[key] = np.column_stack([freq_i,
                                             db_data_i])
        return new_data
    elif isinstance(data, np.ndarray):
        freq = data[:, 0]
        db_data = 20 * np.log10(data[:, -1])
        new_data = np.column_stack([freq,
                                    db_data])
        return new_data
    else:
        return None


def calc_transmissibility(input, output):
    input_data = input[:, -1]
    output_data = output[:, -1]
    xmiss = output_data / input_data
    return np.column_stack([input[:, 0],
                            xmiss])


def apply_transmissibility(input, xmiss, maintain_frequency=False):
    # in future allow input of dict or list
    f_input = input[:, 0]
    f_xmiss = xmiss[:, 0]
    if np.any(f_input != f_xmiss):
        if maintain_frequency:
            xmiss = log_log_interp(f_xmiss, xmiss[:, -1], f_input)
        else:
            input = log_log_interp(f_input, input[:, -1], f_xmiss)
            f_input = input[:, 0]
    new_data = input[:, -1] * xmiss[:, -1]
    output = np.column_stack([f_input,
                              new_data])
    return output


def sdof_transmissibility(fn=None, m=None, k=None, Q=None, units='power',
                          f1=20, f2=2000, df=1, freq=None, limit=None):
    ############################################################################
    if fn is None and (m is None or k is None):
        print('ERROR: If a natural frequency is not provided a '
              'mass in kg and stiffness in N/m needs to me provided.')
        return
    if Q is None:
        print('ERROR: Amplification Q must be provided. Q = 1/(2*zeta).')
        return
    zeta = 1 / (2 * Q)
    if fn is None:
        omegan = np.sqrt(k / m)
        fn = omegan / (2 * np.pi)
    else:
        omegan = 2 * np.pi * fn
    omegan_squared = omegan ** 2
    ############################################################################
    if freq is None:
        # build frequency vector narrowband
        if isinstance(df, int) or isinstance(df, float):
            freq = narrow(f1=f1, f2=f2, df=df)
        else:
            n = float(df)
            freq = octave(f1=f1, f2=f2, n=n)
    ############################################################################
    # accel_xmiss_complex = []
    accel_xmiss_mag = []
    for f in freq:
        omega = 2 * np.pi * f
        omega_squared = omega ** 2

        denominator = (omegan_squared - omega_squared) + (1j) * (
                2 * zeta * omegan * omega)
        numerator = omegan_squared + (1j) * 2 * zeta * omega * omegan

        accel_complex = numerator / denominator
        accel_mag = abs(accel_complex)
        # accel_xmiss_complex.append(accel_complex)
        accel_xmiss_mag.append(accel_mag)

    accel_xmiss_mag = np.asarray(accel_xmiss_mag)
    ############################################################################
    if units in ['power', 'g2/g2', 'psd', 'g^2/g^2']:
        accel_xmiss_mag = accel_xmiss_mag ** 2
    elif units in ['amplitude', 'g/g']:
        accel_xmiss_mag = accel_xmiss_mag
    else:
        print(f'ERROR: {units} is not a valid unit type for a '
              f'transmissibility curve.')
        return

    if limit is not None:
        accel_xmiss_mag = np.where(accel_xmiss_mag < limit,
                                   limit,
                                   accel_xmiss_mag)

    return np.column_stack([freq, accel_xmiss_mag])

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from dynamicly.misc.transmissibility import power_to_dB, amplitude_to_dB


def plot_transmissibility(data, title=None,
                          display_units='g2/g2',
                          input_units='g2/g2'):
    # Perhaps add more units options like power and amplitude (synonyms)
    ############################################################################
    # convert units if needed
    if input_units == display_units:
        data = data
    elif input_units == 'g2/g2' and display_units == 'dB':
        data = power_to_dB(data)
    elif input_units == 'g/g' and display_units == 'dB':
        data = amplitude_to_dB(data)
    else:
        print('Unit mismatch in plot_transmissibility')
        return None
    ############################################################################
    fig, ax = plt.subplots()
    if isinstance(data, dict):
        for key, val in data.items():
            if display_units == 'dB':
                plt.semilogx(val[:, 0], val[:, -1], label=key)
            else:
                plt.loglog(val[:, 0], val[:, -1], label=key)
        ax.legend()
    elif isinstance(data, np.ndarray):
        freq = data[:, 0]
        data = data[:, 1:]
        for col in data.T:
            if display_units == 'dB':
                plt.semilogx(freq, col)
            else:
                plt.loglog(freq, col)
    else:
        return None, None

    ax.set_xlabel('Frequency [Hz]')
    if display_units == 'g2/g2':
        ax.set_ylabel('Transmissibility [$\mathregular{g^{2}/g^{2}}$]')
    if display_units == 'g/g':
        ax.set_xlabel('Natural Frequency [Hz]')
        ax.set_ylabel('Transmissibility [$\mathregular{g/g}$]')
    if display_units == 'dB':
        ax.set_xlabel('Natural Frequency [Hz]')
        ax.set_ylabel('Transmissibility [dB]')
    # ax.grid(which='both', color=[0.9, 0.9, 0.9])
    ax.grid(which='both')
    if title is not None:
        ax.set_title(title)

    return fig, ax

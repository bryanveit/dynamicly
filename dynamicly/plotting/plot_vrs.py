import numpy as np
from matplotlib import pyplot as plt


def plot_vrs(data, title=None, q=10, sigma=3):
    fig, ax = plt.subplots()

    if isinstance(data, dict):
        for key, val in data.items():
            plt.loglog(val[:, 0], val[:, -1], label=key)
        ax.legend()
    elif isinstance(data, np.ndarray):
        freq = data[:, 0]
        data = data[:, 1:]
        for col in data.T:
            plt.loglog(freq, col)
    else:
        return None, None

    ax.set_xlabel('Natural Frequency [Hz]')
    if sigma == 'crest': # CREST FACTOR / RAYLEIGH BASED
        sigma_text = ''
    else:
        sigma_text = f'{sigma}$\sigma$ '
    ax.set_ylabel(f'{sigma_text}VRS Acceleration, Q = {q} [g]')
    ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax.set_title(title)
    if len(ax.get_lines()) == 1:
        ax.get_lines()[0].set_color('k')
        if isinstance(data,dict):
            ax.legend()
    return fig, ax
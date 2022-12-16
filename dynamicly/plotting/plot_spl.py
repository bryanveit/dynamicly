import numpy as np
import matplotlib.pyplot as plt


def plot_spl(data, title=None, axis=None):
    if axis is not None:
        ax = axis
        fig = plt.gcf()
    else:
        fig, ax = plt.subplots()

    if isinstance(data, dict):
        for key, val in data.items():
            if 'nolegend' in key:
                ax.semilogx(val[:, 0], val[:, -1], label='_nolegend')
            else:
                ax.semilogx(val[:, 0], val[:, -1], label=key)
        ax.legend()
    elif isinstance(data, np.ndarray):
        freq = data[:, 0]
        data = data[:, 1:]
        for col in data.T:
            ax.semilogx(freq, col)
    else:
        return None, None

    ax.set_xlabel('Frequency [Hz]')
    # ax.set_ylabel(f'SRS Acceleration, Q = {q} [g]')
    mu = f'$\mu$'
    ax.set_ylabel(f'Sound Pressure Level [dB],  ref. 20 {mu}Pa')
    ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax.set_title(title)
    if len(ax.get_lines()) == 1:
        ax.get_lines()[0].set_color('k')
    return fig, ax

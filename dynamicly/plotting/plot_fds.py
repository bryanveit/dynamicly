import numpy as np
import matplotlib.pyplot as plt

def plot_fds(data, title=None, q=10, b=6.4, unit = 'g'):
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
    ax.set_ylabel(f'Damage Index, Q = {q}, b = {b}  [${unit}^{{b}}$]')
    ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax.set_title(title)

    return fig, ax
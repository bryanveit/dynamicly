import numpy as np
import matplotlib
from matplotlib import pyplot as plt


def plot_time(data, title=None, x_unit='s', x_label=None,
              y_unit='g', y_label=None,
              axis=None, legend=None):
    if axis is not None:
        ax = axis
        fig = plt.gcf()
    else:
        fig, ax = plt.subplots()

    if isinstance(data, dict):
        for key, val in data.items():
            if 'nolegend' in key or 'nolabel' in key:
                ax.plot(val[:, 0], val[:, -1], label='_nolegend')
            else:
                ax.plot(val[:, 0], val[:, -1], label=key)
        if legend is None:
            ax.legend(loc='upper right')
        else:
            ax.legend(loc=legend)
    elif isinstance(data, np.ndarray):
        time = data[:, 0]
        data = data[:, 1:]
        for col in data.T:
            ax.plot(time, col)
    else:
        return None, None
    ax.set_xscale('linear')
    ax.set_yscale('linear')

    ax.set_xlabel(f'Time [{x_unit}]')
    ax.set_ylabel(f'Amplitude [{y_unit}]')
    if y_unit == 'g':
        ax.set_ylabel(f'Acceleration [{y_unit}]')
    if y_unit == 'lbf' or y_unit == 'N' or y_unit == 'lb':
        ax.set_ylabel(f'Thrust [{y_unit}]')

    if y_label:
        ax.set_ylabel(f'{y_label} [{y_unit}]')
    if x_label:
        ax.set_xlabel(f'{x_label} [{x_unit}]')
    # ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax.set_title(title)

    if len(ax.get_lines()) == 1:
        ax.get_lines()[0].set_color('k')
        if isinstance(data, dict):
            if legend is None:
                ax.legend(loc='upper right')
            else:
                ax.legend(loc=legend)
    for line in ax.get_lines():
        line.set_linewidth(0.5)
    ax.grid(which='both', color=[0.9, 0.9, 0.9])
    return fig, ax


def plot_time_windows(data, time_windows,
                      title=None, x_unit='s', x_label=None,
                      y_unit='g', y_label=None,
                      axis=None, legend=None, cmap=None):
    if axis is not None:
        ax = axis
        fig = plt.gcf()
    else:
        fig, ax = plt.subplots()

    if isinstance(data, dict):
        return None, None
    elif isinstance(data, np.ndarray):
        time = data[:, 0]
        mag = data[:, -1]
        # ax.plot(time, mag, color='k')
        ax.plot(time, mag, color=[.5, .5, .5])

        if cmap is None:
            waterfall = plt.cm.coolwarm(np.linspace(0, 1, len(time_windows)))
        else:
            waterfall = cmap(np.linspace(0, 1, len(time_windows)))
        # # waterfall = plt.cm.gist_earth(np.linspace(0, 1, len(time_windows)))
        # waterfall = plt.cm.flag(np.linspace(0, 1, len(time_windows)))
        for i, win_plot in enumerate(time_windows):
            ax.plot(win_plot[:, 0],
                    win_plot[:, -1],
                    color=waterfall[i],
                    linewidth=0.5)

    else:
        return None, None
    ax.set_xscale('linear')
    ax.set_yscale('linear')

    ax.set_xlabel(f'Time [{x_unit}]')
    ax.set_ylabel(f'Amplitude [{y_unit}]')
    if y_unit == 'g':
        ax.set_ylabel(f'Acceleration [{y_unit}]')
    if y_unit == 'lbf' or y_unit == 'N' or y_unit == 'lb':
        ax.set_ylabel(f'Thrust [{y_unit}]')

    if y_label:
        ax.set_ylabel(f'{y_label} [{y_unit}]')
    if x_label:
        ax.set_xlabel(f'{x_label} [{x_unit}]')
    # ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax.set_title(title)

    if len(ax.get_lines()) == 1:
        ax.get_lines()[0].set_color('k')
        if isinstance(data, dict):
            if legend is None:
                ax.legend(loc='upper right')
            else:
                ax.legend(loc=legend)
    for line in ax.get_lines():
        line.set_linewidth(0.5)
    ax.grid(which='both', color=[0.9, 0.9, 0.9])
    return fig, ax


def plot_secondary_axis(data1, data2, x_unit='s',
                        y_unit1=' ', y_unit2=' ',
                        y_label1='Amplitude', y_label2='Amplitude',
                        title=None, axis=None, legend=None):
    if axis is not None:
        ax1 = axis
        fig = plt.gcf()
    else:
        fig, ax1 = plt.subplots()

    if isinstance(data1, dict):
        for key, val in data1.items():
            if 'nolegend' in key:
                ax1.plot(val[:, 0], val[:, -1], label='_nolegend')
            else:
                ax1.plot(val[:, 0], val[:, -1], label=key)
        if legend is None:
            ax1.legend(loc='upper right')
        else:
            ax1.legend(loc=legend)
    elif isinstance(data1, np.ndarray):
        time = data1[:, 0]
        data = data1[:, 1:]
        for col in data.T:
            ax1.plot(time, col)
    else:
        return None, None

    ax2 = ax1.twinx()
    if isinstance(data2, dict):
        for key, val in data2.items():
            if 'nolegend' in key:
                ax2.plot(val[:, 0], val[:, -1], label='_nolegend')
            else:
                ax2.plot(val[:, 0], val[:, -1], label=key)
        if legend is None:
            ax2.legend(loc='upper right')
        else:
            ax2.legend(loc=legend)
    elif isinstance(data2, np.ndarray):
        time = data2[:, 0]
        data = data2[:, 1:]
        for col in data.T:
            ax2.plot(time, col)
    else:
        return None, None

    ax1.set_xscale('linear')
    ax1.set_yscale('linear')
    ax2.set_xscale('linear')
    ax2.set_yscale('linear')

    ax1.set_xlabel(f'Time [{x_unit}]')
    ax1.set_ylabel(f'{y_label1} [{y_unit1}]')
    ax2.set_ylabel(f'{y_label2} [{y_unit2}]')

    # ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax1.set_title(title)
    #
    # if len(ax1.get_lines()) == 1:
    #     ax1.get_lines()[0].set_color('k')
    #     if isinstance(data, dict):
    #         if legend is None:
    #             ax.legend(loc='upper right')
    #         else:
    #             ax.legend(loc=legend)
    # for line in ax.get_lines():
    #     line.set_linewidth(0.5)
    ax1.get_lines()[0].set_color('k')
    i = 2
    for line1, line2 in zip(ax1.get_lines(), ax2.get_lines()):
        line1.set_zorder(2 * i - 1)
        line2.set_zorder(2 * i)
        # print(2*i-1)
        # print(2 * i)
        i += 1
    ax1.grid(which='both', color=[0.9, 0.9, 0.9], zorder=0)
    ax2.grid(False)
    plt.rc('axes', axisbelow=True)
    try:
        test = ax1.get_lines()[1]
        ax1.legend(loc=2, fontsize=8)
    except:
        if y_label1 == 'Amplitude':
            y_label1 = 'Left Axis'
        ax1.get_lines()[0].set_label(y_label1)
        ax1.legend(loc=2, fontsize=8)
    try:
        test = ax2.get_lines()[1]
        ax2.legend(loc=1)
    except:
        if y_label2 == 'Amplitude':
            y_label2 = 'Right Axis'
        ax2.get_lines()[0].set_label(y_label2)
        ax2.legend(loc=1, fontsize=8)
    # make sure o0 matches up later
    return fig, (ax1, ax2)

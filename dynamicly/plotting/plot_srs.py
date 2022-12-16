import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from dynamicly.plotting.plot_time import plot_time
from dynamicly.utils.srs import calc_srs


def constant_velocity_lines(axis, velocities=(50, 100, 300), units='in/s',
                            color=None, fontsize=7, angle=35):
    orig_x_lim = axis.get_xlim()
    orig_y_lim = axis.get_ylim()

    first_line_order = axis.get_lines()[0].get_zorder()

    if units == 'ips' or units == 'in/s':
        factor = 1 / 386.1  # to g
        unit_label = 'ips'
    else:
        # THIS IS TEMPORARY
        # factor = 1 / 386.1  # to g
        # unit_label = 'ips'
        pass

    x = np.array([.01, 100000])

    if color is None:
        color = [0.7, 0.7, 0.7]
    style = '-'

    for v in velocities:
        y = 2 * np.pi * x * v * factor
        line = np.column_stack([x, y])
        axis.loglog(line[:, 0], line[:, -1],
                    linewidth=.5,
                    color=color,
                    linestyle=style,
                    zorder=first_line_order - 1)
        label = f'{v} {unit_label}'
        # OUTSIDE AXES
        # y_label = orig_y_lim[-1] * 1.02
        # x_label = y_label / (2 * np.pi * v * factor)
        # INSIDE AXES
        y_label = orig_y_lim[-1] / 1.25
        x_label = y_label / (2 * np.pi * v * factor)
        x_label = x_label / 1.11


        y_label = orig_y_lim[-1] / 1.45
        x_label = y_label / (2 * np.pi * v * factor)
        x_label = x_label / 1.15

        # y_label = orig_y_lim[-1] / 1.8
        # x_label = y_label / (2 * np.pi * v * factor)
        # x_label = x_label / 1.2

        # yy = np.log10(np.diff(orig_y_lim))[0]
        # xx = np.log10(np.diff(orig_x_lim))[0]
        # angle = np.arctan(yy/xx)*180/np.pi
        # angle = angle + (np.arctan(27/20)*180/np.pi-45)\
        axis.text(x_label, y_label, label, rotation=angle, fontsize=fontsize)

    axis.set_xlim(orig_x_lim)
    axis.set_ylim(orig_y_lim)
    axis.set_axisbelow(True)
    return


def plot_srs(data, title=None, q=10, axis=None, velocity_lines = False):
    if axis is not None:
        ax = axis
        fig = plt.gcf()
    else:
        fig, ax = plt.subplots()

    if isinstance(data, dict):
        for key, val in data.items():
            if 'nolegend' in key or 'nolabel' in key:
                ax.loglog(val[:, 0], val[:, -1], label='_nolegend')
            else:
                ax.loglog(val[:, 0], val[:, -1], label=key)
        ax.legend()
    elif isinstance(data, np.ndarray):
        freq = data[:, 0]
        data = data[:, 1:]
        for col in data.T:
            ax.loglog(freq, col)
    else:
        return None, None

    ax.set_xlabel('Natural Frequency [Hz]')
    # ax.set_ylabel(f'SRS Acceleration, Q = {q} [g]')
    ax.set_ylabel(f'SRS Acceleration [g],  Q = {q}')
    ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax.set_title(title)
    if len(ax.get_lines()) == 1:
        ax.get_lines()[0].set_color('k')
    if velocity_lines:
        constant_velocity_lines(ax)
    return fig, ax


def plot_srs_spec(data, title=None, q=10, table_fontsize=9, col_width=0.25):
    fig, (ax, tab) = plt.subplots(2, 1)
    fig.set_size_inches(8.5, 11)

    for key, val in data.items():
        ax.loglog(val[:, 0], val[:, -1], label=key)
    ax.legend()
    ax.set_xlabel('Natural Frequency [Hz]')
    ax.set_ylabel(f'SRS Acceleration [g],  Q = {q}')
    ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax.set_title(title)
    if len(ax.get_lines()) == 1:
        ax.get_lines()[0].set_color('k')
    tab.axis('off')
    # QTP only capability first
    # spec_levels = {key:val for key,val in data.items() if key in ['ATP','QTP']}

    spec_levels = {key: val for key, val in data.items() if 'QTP' in key}
    # cols = ['Frequency [Hz]', f'QTP SRS, Q = {q} [g]']
    cols = ['Frequency [Hz]', f'QTP SRS [g],  Q = {q}']
    # cols = ['Frequency [Hz]', f'QTP [g],  Q = {q}']
    data_table = spec_levels[list(spec_levels.keys())[0]]

    freq = list(data_table[:, 0])
    srs = list(data_table[:, -1])

    freq = ['%d' % i for i in freq]
    srs_rounded = ['%d' % i for i in srs]
    # for raw in srs:
    #     # place = np.floor(np.log10(raw))
    #     # place = int(np.abs(place) + 2)
    #     # rounded = np.round(raw)
    #     rounded = int(raw)
    #     srs_rounded.append(rounded)

    data_table = []
    for i, f in enumerate(freq):
        p = f'{srs_rounded[i]}'
        new_row = [f, p]
        data_table.append(new_row)
    # the_table = tab.table(
    #     cellText=data_table, colLabels=cols, loc='bottom',
    #     rowLoc='center', colLoc='center', colWidths=[0.3, 0.3],
    # )
    hits_row = ['', '3 hits/axis']
    data_table.append(hits_row)

    light_gray = [.7, .7, .7]
    # colWidths = [0.3, 0.3]
    if col_width:
        colWidths = [col_width, col_width]
    else:
        colWidths = [0.17, 0.17]
    the_table = tab.table(
        cellText=data_table, colLabels=cols, loc='center',
        rowLoc='center', colLoc='center', colWidths=colWidths,
        # fontsize=12,
        # fontsize=table_fontsize,
        colColours=[light_gray, light_gray]
    )

    table_props = the_table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells: cell.set_height(0.08)
    for cell in table_cells: cell._loc = 'center'
    open = False
    for cell in table_cells:
        if cell._text._text == '':
            open = True
        if 'hits' in cell._text._text:
            open = True
        if 'Freq' in cell._text._text:
            open = False
            # again
        if open:
            cell._edges = 'open'

    # the_table.set_fontsize(10)
    if table_fontsize:
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(table_fontsize)
    fig.subplots_adjust(left=0.2, right=0.85)

    pos1 = ax.get_position().get_points()
    pos2 = tab.get_position().get_points()

    # fig.subplots_adjust(hspace=0.4)
    # tab.set_position([0.025, -.31, 1, .5])
    return fig, ax, tab


def plot_time_and_srs(time_history, srs=None, Q=10, fn=None, title=None,
                      fig_size=(8.5, 11)):
    if srs is None:
        # This assumes the input is time history and the srs will
        srs = calc_srs(time_history, Q=Q, fn=fn)
    fig, (ax_time, ax_srs) = plt.subplots(2)
    fig, ax_time = plot_time(time_history, axis=ax_time)
    fig, ax_srs = plot_srs(srs, axis=ax_srs)
    fig.set_size_inches(fig_size[0], fig_size[1])
    if title is not None:
        ax_time.set_title(title)
    return fig, (ax_time, ax_srs)

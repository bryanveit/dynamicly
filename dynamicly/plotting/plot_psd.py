import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from dynamicly.calc_rms import calc_rms
from dynamicly.maximax import maximax
from dynamicly.quick_dictionary import quick_dict

from dynamicly import plotting as plot
from dynamicly.utils.psd import calc_psd_windows, calc_psd
from dynamicly import levels


def plot_psd(data, title=None, axis=None, xlim=None):
    if axis is not None:
        ax = axis
        fig = plt.gcf()
    else:
        fig, ax = plt.subplots()

    if isinstance(data, dict):
        for key, val in data.items():
            plt.loglog(val[:, 0], val[:, -1], label=key)
            # ax.legend()
            # print('debug')
        ax.legend()
    elif isinstance(data, np.ndarray):
        freq = data[:, 0]
        data = data[:, 1:]
        for col in data.T:
            plt.loglog(freq, col)
    else:
        return None, None
    if xlim is not None:
        ax.set_xlim(xlim)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Power Spectral Density [$\mathregular{g^{2}/Hz}$]')
    ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax.set_title(title)
    if len(ax.get_lines()) == 1:
        ax.get_lines()[0].set_color('k')
    return fig, ax


# Idealy this would utilize plot_psd but I am not entirely sure how axes and
# figures work in matplotlib to add a table beneath exisiting plot
def plot_psd_spec(data, title=None, sigfigs=3, rms_decimals=1,
                  atp_duraiton=60, qtp_duration=180,
                  duration_unit='s', colors='Firefly'):
    fig, (ax, tab) = plt.subplots(2, 1)
    fig.set_size_inches(8.5, 11)

    for key, val in data.items():
        if 'nolegend' in key:
            if 'upper' in key or 'lower' in key:
                ax.loglog(val[:, 0], val[:, -1],
                          label='_nolegend',
                          linestyle=':',
                          color=plot.gray)
            else:
                ax.loglog(val[:, 0], val[:, -1], label='_nolegend')
        else:
            ax.loglog(val[:, 0], val[:, -1], label=key)

    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Power Spectral Density [$\mathregular{g^{2}/Hz}$]')
    ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if len(ax.get_lines()) == 1:
        ax.get_lines()[0].set_color('k')
    else:
        for line in ax.get_lines():
            if 'QTP' in line.get_label():
                line.set_color('k')
                line.set_linewidth(2)
            if 'ATP' in line.get_label():
                line.set_color(plot.gray)
                line.set_linewidth(2)
    if title is not None:
        ax.set_title(title)
    ax.legend()
    tab.axis('off')

    try:
        ymin = min(data['ATP'][:,-1])/2
        ymax = max(data['QTP'][:,-1])*2
        ax.set_ylim(ymin,ymax)
    except:
        ax.set_ylim(1e-4,1)
    ############################################################################
    # QTP only capability first
    spec_levels = {key: val for key, val in data.items() if
                   key in ['ATP', 'QTP']}
    # spec_levels = {key: val for key, val in data.items() if 'QTP' in key}
    other_cols = [f'{key}' + ' [$\mathregular{g^{2}/Hz}$]'
                  for key in list(spec_levels.keys())]
    other_cols.sort()
    cols = ['Frequency [Hz]', *other_cols]
    # cols = ['Frequency [Hz]', 'QTP [$\mathregular{g^{2}/Hz}$]']
    # cols = ['Frequency [Hz]', 'ATP [$\mathregular{g^{2}/Hz}$]']

    # this makes up the table
    # data_table = spec_levels[list(spec_levels.keys())[0]]
    # add freq
    data_table = spec_levels[list(spec_levels.keys())[0]][:, 0]
    # add psd
    # for key, val in spec_levels.items():
    for key in other_cols:
        key = key.split(' ')[0]
        val = spec_levels[key]
        spec_column = val[:, -1]
        data_table = np.column_stack([data_table,
                                      spec_column])

    freq_np = list(data_table[:, 0])
    freq = ['%d' % i for i in freq_np]
    data_table_clean = []

    psd_values = data_table[:, 1:]

    for i, row_of_psd in enumerate(psd_values):
        psd = list(row_of_psd)
        psd_rounded = []
        for raw in psd:
            place = np.floor(np.log10(raw))
            place = int(np.abs(place) + (sigfigs - 1))
            rounded = np.round(raw, place)
            psd_rounded.append(rounded)

        f = freq[i]
        psd_strings = [f'{p}' for p in psd_rounded]
        new_row = [f, *psd_strings]
        data_table_clean.append(new_row)

    # the_table = tab.table(
    #     cellText=data_table, colLabels=cols, loc='bottom',
    #     rowLoc='center', colLoc='center', colWidths=[0.3, 0.3],
    # )
    rms_row = ['gRMS:']
    for col in psd_values.T:
        rms = calc_rms(np.column_stack([freq_np,
                                        col]))
        rms = f'{np.round(rms, rms_decimals)}'
        rms_row.append(rms)

    duration_row = ['Duration:']
    for key in other_cols:
        if 'ATP' in key:
            duration_row.append(f'{atp_duraiton} {duration_unit}')
        elif 'QTP' in key:
            duration_row.append(f'{qtp_duration} {duration_unit}')
        else:
            duration_row.append('---')

    data_table_clean.append(rms_row)
    data_table_clean.append(duration_row)

    light_gray = [.7, .7, .7]
    the_table = tab.table(
        cellText=data_table_clean, colLabels=cols, loc='center',
        rowLoc='center', colLoc='center', colWidths=[0.2, 0.25, 0.25],
        colColours=[light_gray, light_gray, light_gray]
    )
    table_props = the_table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells: cell.set_height(0.06)
    for cell in table_cells: cell._loc = 'center'
    open = False
    for cell in table_cells:
        if 'RMS' in cell._text._text:
            cell._loc = 'right'
            open = True
        if 'Dur' in cell._text._text:
            cell._loc = 'right'
            open = True
        if 'Freq' in cell._text._text:
            open = False
            # again
        if open:
            cell._edges = 'open'

    the_table.set_fontsize(9)
    fig.subplots_adjust(left=0.2, right=0.85)

    pos1 = ax.get_position().get_points()
    pos2 = tab.get_position().get_points()

    # fig.subplots_adjust(hspace=0.4)
    # tab.set_position([0.025, -.31, 1, .5])
    return fig, ax, tab


def grms_labels(dictionary):
    new_dict = {f'{key}   ({calc_rms(val, round=1)} gRMS)': val for key, val in
                dictionary.items()}
    return new_dict


def plot_psd_waterfall(psd_windows, title=None, axis=None,
                       psd_max=None, plot_max=True,
                       plot_smc=True, cmap = None):
    if axis is not None:
        ax = axis
        fig = plt.gcf()
    else:
        fig, ax = plt.subplots()

    if cmap is None:
        waterfall = plt.cm.coolwarm(np.linspace(0, 1, len(psd_windows)))
    else:
        waterfall = cmap(np.linspace(0, 1, len(psd_windows)))

    # waterfall = plt.cm.gist_earth(np.linspace(0, 1, len(psd_windows)))
    # waterfall = plt.cm.cool(np.linspace(0, 1, len(psd_windows)))
    # waterfall = plt.cm.gnuplot(np.linspace(0, 1, len(psd_windows)))
    # waterfall = plt.cm.rainbow(np.linspace(0, 1, len(psd_windows)))
    for i, win_plot in enumerate(psd_windows):
        ax.loglog(win_plot[:, 0],
                  win_plot[:, -1],
                  color=waterfall[i],
                  linewidth=0.5)
        # print(i+1)
        # print('debug')
    if plot_max:
        if psd_max is None:
            psd_max = maximax(quick_dict(psd_windows))
        ax.loglog(psd_max[:, 0],
                  psd_max[:, -1],
                  color='k',
                  linewidth=2,
                  # label='Maximum'
                  )

    if plot_smc:
        ax.loglog(levels.smc()[:, 0],
                  levels.smc()[:, -1],
                  color='k',
                  linewidth=2,
                  # label='Maximum'
                  )
        # ax.legend()
    ax.set_xlim(20, 2000)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Power Spectral Density [$\mathregular{g^{2}/Hz}$]')
    # ax.grid(which='both', color=[0.9, 0.9, 0.9])
    if title is not None:
        ax.set_title(title)
    if len(ax.get_lines()) == 1:
        ax.get_lines()[0].set_color('k')

    return fig, ax


def plot_psd_duo(time_history, psd_windows=None, psd_max=None, title=None,
                 full_time_history=None, time_windows=None, cmap=None):
    if psd_windows is None:
        psd_windows = calc_psd_windows(time_history, return_max=False)

    if psd_max is None:
        psd_max = maximax(quick_dict(psd_windows))
    psd_average = calc_psd(time_history)

    fig = plt.figure()
    gs = fig.add_gridspec(3, 1)
    ax1 = fig.add_subplot(gs[:1, :])
    ax2 = fig.add_subplot(gs[1:, :])
    # fig, (ax1, ax2) = plt.subplots(2)

    plt.subplots_adjust(hspace=0.4, top=0.8, bottom=0.2)
    fig.set_size_inches(8.5, 11)

    if time_windows:
        fig, ax1 = plot.plot_time_windows(time_history,
                                          time_windows=time_windows,
                                          title=title,
                                          axis=ax1,
                                          cmap=cmap)
    else:
        fig, ax1 = plot.plot_time(time_history, title=title, axis=ax1)
    fig, ax2 = plot_psd_waterfall(psd_windows, axis=ax2, psd_max=psd_max,
                                  cmap=cmap)
    # fig, ax2 = plot.plot_psd(psd_max,axis=ax2)
    # ax2.get_lines()[-1].set_color('k')
    # ax2.set_xlim(20, 2000)
    if full_time_history is not None:
        ax1.get_lines()[0].set_color('k')
        ax1.get_lines()[0].set_zorder(100)
        fig, ax1 = plot.plot_time(full_time_history, title=title, axis=ax1)
        ax1.get_lines()[1].set_zorder(99)
        ax1.get_lines()[1].set_color(plot.gray)

    return fig, (ax1, ax2)


def plot_psd_trio(time_history, psd_windows=None, psd_max=None, title=None,
                  calc_time_history=None, full_time_history=None):
    if psd_windows is None:
        psd_windows = calc_psd_windows(time_history, return_max=False)

    if psd_max is None:
        psd_max = maximax(quick_dict(psd_windows))
    psd_average = calc_psd(time_history)

    fig, (ax1, ax2, ax3) = plt.subplots(3)

    plt.subplots_adjust(hspace=0.3)
    fig.set_size_inches(8.5, 11)

    fig, ax1 = plot.plot_time(time_history, title=title, axis=ax1)
    if calc_time_history is not None:
        ax1.get_lines()[0].set_color(plot.gray)
        fig, ax1 = plot.plot_time(calc_time_history, title=title, axis=ax1)
        ax1.get_lines()[1].set_color('k')

    if full_time_history is not None:
        ax1.get_lines()[0].set_color('k')
        ax1.get_lines()[0].set_zorder(100)
        fig, ax1 = plot.plot_time(full_time_history, title=title, axis=ax1)
        ax1.get_lines()[1].set_zorder(99)
        ax1.get_lines()[1].set_color(plot.gray)

    fig, ax2 = plot_psd_waterfall(psd_windows, axis=ax2, psd_max=psd_max)
    # fig, ax2 = plot.plot_psd(psd_max,axis=ax2)
    # ax2.get_lines()[-1].set_color('k')
    ax2.set_xlim(20, 2000)
    # ax2.set_ylim(1e-3, 10)
    ax2.set_ylim(1e-4, 2)
    plot3 = {
        'Maximax': psd_max,
        'Average': psd_average,
        'SMC-S-016 Minimum Workmaship': levels.smc()
    }

    fig, ax3 = plot_psd(plot3, axis=ax3)
    ax3.set_xlim(20, 2000)
    # ax3.set_ylim(1e-3, 10)
    ax3.set_ylim(1e-4, 2)
    ax3.get_lines()[0].set_color('k')
    ax3.get_lines()[0].set_linewidth(2)
    ax3.get_lines()[0].set_zorder(99)
    ax3.get_lines()[1].set_color(plot.gray)
    ax3.get_lines()[0].set_zorder(100)

    ax3.get_lines()[2].set_color(plot.gray * 1.1)
    ax3.get_lines()[2].set_linestyle(':')
    ax3.legend()

    return fig, (ax1, ax2, ax3)


# def rms_dict_keys(dictionary):
#     dyn.calc

if __name__ == '__main__':
    # plt.rcParams["font.family"] = "Times New Roman"
    # # atp = np.column_stack([[20, 150, 200, 205, 210, 215, 220, 225, 230, 235],
    # #                        [.055, .1, .1,.3,.3,.3,.3,.3,.3,.3]])
    # atp = np.column_stack([[20, 150, 2000],
    #                        [.055, .100000000006, .1]])
    # qtp = np.column_stack([atp[:, 0],
    #                        atp[:, -1] * 4])
    #
    # plot_dict = {
    #     'QTP': qtp,
    #     'ATP': atp,
    # }
    #
    # f, a, t = plot_psd_spec(plot_dict)

    from dynamicly.io import loadmat

    time = loadmat('../sample files/R3-AXFPH-RAD-D.mat')['time']
    fig, axes = plot_psd_duo(time)

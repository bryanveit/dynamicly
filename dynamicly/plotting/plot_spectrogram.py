from matplotlib import pyplot as plt
from dynamicly.signal.sample_rate import calc_sample_rate
import numpy as np
from dynamicly.plotting import plot_time
import dynamicly.plotting as plot

def plot_spectrogram(time_history, df=10, overlap=0.9, x_unit='s',
                     scale_for_noise=False, colorbar=False, power2=True,
                     colormap=None, title=None, adjust_time=True,
                     axis=None, return_xticks=False, scale = 'default',
                     mode='psd'):
    fs = calc_sample_rate(time_history)
    n = len(time_history)
    time = time_history[:, 0]
    mag = time_history[:, -1]

    if isinstance(df, str):
        nfft = int(np.round(fs * float(df)))
        if power2:
            nfft = 2 ** int(np.log2(nfft))
        print(
            f'String input for {df} {x_unit} windows => {np.round(nfft / fs, 3)} {x_unit} windows  => frequency resolution, df = {np.round(fs / nfft, 2)} Hz.\n')
    else:
        nfft = np.round(fs / df)
        if power2:
            nfft = 2 ** int(np.log2(nfft))
    noverlap = np.round(nfft * overlap)

    if axis is not None:
        ax = axis
        fig = plt.gcf()
    else:
        fig, ax = plt.subplots()
    if colormap is None:
        cmap = plt.get_cmap('viridis')
        cmap.set_under(color='k', alpha=None)

    else:
        cmap = plt.get_cmap(colormap)

    Pxx, freqs, bins, im = ax.specgram(mag, NFFT=nfft, Fs=fs,
                                       noverlap=noverlap, mode=mode,
                                       scale=scale, cmap=cmap)
    if colorbar:
        plt.colorbar(mappable=im)
    if scale_for_noise:
        lower = np.mean(10 * np.log10(Pxx))
        if isinstance(scale_for_noise, float):
            lower = lower + scale_for_noise * np.std(10 * np.log10(Pxx))
        upper = np.max(10 * np.log10(Pxx))
        im.set_clim(lower, upper)
    ax.set_xlabel(f'Time [{x_unit}]')
    ax.set_ylabel(f'Frequency [Hz]')

    if adjust_time:
        if abs(time[0]) > 0.01:
            locs, tick_labels = plt.xticks()
            if locs[-1] > time[-1]:
                locs = locs[:-1]
            dt = locs[1] - locs[0]
            shift = locs
            new_labels = []
            for i, num in enumerate(shift):
                if np.round(time[0] + i * dt, 2) > time[-1]:
                    continue
                new_labels.append(f'{np.round(time[0] + i * dt, 2)}')
            plt.xticks(ticks=shift, labels=new_labels)

    if title is not None:
        ax.set_title(title)

    if return_xticks:
        if adjust_time:
            return fig, ax, (shift, new_labels)
        else:
            locs, tick_labels = plt.xticks()
            return fig, ax, (locs, tick_labels)
    else:
        return fig, ax


def plot_time_and_spectrogram(time_history, df=10, overlap=0.9, x_unit='s',
                              scale_for_noise=False, colorbar=False,
                              power2=True, colormap=None, title=None,
                              adjust_time=True, fig_size=(8.5, 10),
                              time_color = 'k', scale='default',
                              mode='psd'):
    fig = plt.figure()
    gs = fig.add_gridspec(4, 1)
    ax_time = fig.add_subplot(gs[:1, :])
    ax_spectrogram = fig.add_subplot(gs[1:, :])
    # fig, (ax_time, ax_spectrogram) = plt.subplots(2)

    fig, ax_time = plot_time(time_history, axis=ax_time)

    fig, ax_spectrogram, labels = plot_spectrogram(
        time_history=time_history,
        df=df,
        overlap=overlap,
        x_unit=x_unit,
        scale_for_noise=scale_for_noise,
        colorbar=colorbar,
        power2=power2,
        colormap=colormap,
        title=None,
        adjust_time=adjust_time,
        axis=ax_spectrogram,
        return_xticks=True,
        scale = scale,
        mode=mode,
    )
    fig.set_size_inches(fig_size[0], fig_size[1])

    spec_true_range = (time_history[0,0],time_history[-1,0])
    spec_mpl_range = ax_spectrogram.get_xlim()
    spec_tick_coord = labels[0]
    spec_tick_text = labels[1]

    time_range = (
        float(spec_tick_text[0]),
        spec_true_range[1],
    )
    ax_time.set_xlim(*time_range)
    ax_time.xaxis.tick_top()
    ax_time.xaxis.set_label_position('top')
    plt.subplots_adjust(hspace=0.04)

    if time_color is not 'k':
        ax_time.set_facecolor('k')
        ax_time.get_lines()[0].set_color(time_color)

    else:
        ax_time.set_facecolor(plot.white)
        ax_time.get_lines()[0].set_color(time_color)

    if title is not None:
        ax_time.set_title(title, pad=20, fontweight='bold')

    ax_spectrogram.set_facecolor('k')
    if cmap.name is 'binary':
        ax_spectrogram.set_facecolor('w')
    return fig, (ax_time, ax_spectrogram)

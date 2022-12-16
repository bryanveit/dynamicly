import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams["font.family"] = "Arial"
plt.rcParams['grid.color'] = [0.8, 0.8, 0.8]
plt.rcParams['grid.linestyle'] = ':'

some_fonts = {
    'times': 'Times New Roman',
    'arial': 'Arial',
    'arial b': 'Arial Black',
    'arial bold': 'Arial Black',
    'arial black': 'Arial Black',
    'oswald': 'Oswald',
    'courier': 'Courier New',
    'courier new': 'Courier New',
    'trebuchet': 'Trebuchet MS',
    'lucida': 'Lucida Console',
    'consolas': 'Consolas',
    'beepboop': 'Consolas',
}


def change_font(fam):
    if fam in list(some_fonts.keys()):
        fam = some_fonts[fam]
    try:
        plt.rcParams['font.family'] = fam
        return
    except:
        return


# COLORS

black = np.asarray([0, 0, 0])
white = np.asarray([1, 1, 1])

bug_green = [189, 220, 0]
bug_green = bug_green / np.linalg.norm(bug_green)

crimson = [50, 0, 0]
crimson = crimson / np.linalg.norm(crimson)

purple = [148 * .9, 0, 211 * .9]
purple = [val * .9 for val in purple]
purple = purple / np.linalg.norm(purple)

indigo = [56, 52, 70]
indigo = indigo / np.linalg.norm(indigo)

indigo_dark = [56 / 255, 52 / 255, 70 / 255]

# match matlab
pink = [255, 0, 255]
pink = pink / np.linalg.norm(pink)

green = [0, 255, 0]
green = green / np.linalg.norm(green)

gray = [0.5, 0.5, 0.5]
gray = gray / np.linalg.norm(gray)

orange = [255, 140, 0]
orange = orange / np.linalg.norm(orange)

cyan = [0, 255, 255]
cyan = cyan / np.linalg.norm(cyan)


def dark_mode():
    plt.style.use('dark_background')
    return


def black_line(axis, index=-1, lw=2, zorder=None):
    axis.get_lines()[index].set_color('k')
    axis.get_lines()[index].set_linewidth(lw)
    if zorder is not None:
        axis.get_lines()[index].set_zorder(zorder)
    if len(axis.get_lines()) > 1:
        axis.legend()
    return


def gray_line(axis, index=-1, lw=2, scale=1):
    if scale > 1:
        scale = 1
    axis.get_lines()[index].set_color(gray * scale)
    axis.get_lines()[index].set_linewidth(lw)
    if len(axis.get_lines()) > 1:
        axis.legend()
    return


def crimson_line(axis, index=-1, lw=2):
    axis.get_lines()[index].set_color(crimson)
    axis.get_lines()[index].set_linewidth(lw)
    if len(axis.get_lines()) > 1:
        axis.legend()
    return


def bug_line(axis, index=-1, lw=2, scale=1):
    if scale > 1:
        scale = 1
    axis.get_lines()[index].set_color(bug_green * scale)
    axis.get_lines()[index].set_linewidth(lw)
    if len(axis.get_lines()) > 1:
        axis.legend()
    return


def indigo_line(axis, index=-1, lw=1):
    axis.get_lines()[index].set_color(indigo)
    axis.get_lines()[index].set_linewidth(lw)
    if len(axis.get_lines()) > 1:
        axis.legend()
    return


def dash_line(axis, index=-1):
    axis.get_lines()[index].set_linestyle('--')
    if len(axis.get_lines()) > 1:
        axis.legend()
    return


def dot_line(axis, index=-1):
    axis.get_lines()[index].set_linestyle(':')
    if len(axis.get_lines()) > 1:
        axis.legend()
    return


def purple_line(axis, index=-1, lw=2):
    axis.get_lines()[index].set_color(purple)
    axis.get_lines()[index].set_linewidth(lw)
    if len(axis.get_lines()) > 1:
        axis.legend()
    return


def color_cycle(first='deep'):
    if first == 'deep':
        cycle = [
            # 'k',
            # sns.color_palette('deep')
            (0.2980392156862745, 0.4470588235294118, 0.6901960784313725),
            (0.8666666666666667, 0.5176470588235295, 0.3215686274509804),
            (0.3333333333333333, 0.6588235294117647, 0.40784313725490196),
            (0.7686274509803922, 0.3058823529411765, 0.3215686274509804),
            (0.5058823529411764, 0.4470588235294118, 0.7019607843137254),
            (0.5764705882352941, 0.47058823529411764, 0.3764705882352941),
            (0.8549019607843137, 0.5450980392156862, 0.7647058823529411),
            (0.5490196078431373, 0.5490196078431373, 0.5490196078431373),
            (0.8, 0.7254901960784313, 0.4549019607843137),
            (0.39215686274509803, 0.7098039215686275, 0.803921568627451),
            # sns.color_palette('dark')
            (0.0, 0.10980392156862745, 0.4980392156862745),
            (0.6941176470588235, 0.25098039215686274, 0.050980392156862744),
            (0.07058823529411765, 0.44313725490196076, 0.10980392156862745),
            (0.5490196078431373, 0.03137254901960784, 0.0),
            (0.34901960784313724, 0.11764705882352941, 0.44313725490196076),
            (0.34901960784313724, 0.1843137254901961, 0.050980392156862744),
            (0.6352941176470588, 0.20784313725490197, 0.5098039215686274),
            (0.23529411764705882, 0.23529411764705882, 0.23529411764705882),
            (0.7215686274509804, 0.5215686274509804, 0.0392156862745098),
            (0.0, 0.38823529411764707, 0.4549019607843137),
        ]
    if first == 'dark':
        cycle = [
            'k',
            # sns.color_palette('dark')
            (0.0, 0.10980392156862745, 0.4980392156862745),
            (0.6941176470588235, 0.25098039215686274, 0.050980392156862744),
            (0.07058823529411765, 0.44313725490196076, 0.10980392156862745),
            (0.5490196078431373, 0.03137254901960784, 0.0),
            (0.34901960784313724, 0.11764705882352941, 0.44313725490196076),
            (0.34901960784313724, 0.1843137254901961, 0.050980392156862744),
            (0.6352941176470588, 0.20784313725490197, 0.5098039215686274),
            (0.23529411764705882, 0.23529411764705882, 0.23529411764705882),
            (0.7215686274509804, 0.5215686274509804, 0.0392156862745098),
            (0.0, 0.38823529411764707, 0.4549019607843137),
            # sns.color_palette('deep')
            (0.2980392156862745, 0.4470588235294118, 0.6901960784313725),
            (0.8666666666666667, 0.5176470588235295, 0.3215686274509804),
            (0.3333333333333333, 0.6588235294117647, 0.40784313725490196),
            (0.7686274509803922, 0.3058823529411765, 0.3215686274509804),
            (0.5058823529411764, 0.4470588235294118, 0.7019607843137254),
            (0.5764705882352941, 0.47058823529411764, 0.3764705882352941),
            (0.8549019607843137, 0.5450980392156862, 0.7647058823529411),
            (0.5490196078431373, 0.5490196078431373, 0.5490196078431373),
            (0.8, 0.7254901960784313, 0.4549019607843137),
            (0.39215686274509803, 0.7098039215686275, 0.803921568627451),
        ]
    if first == 'ff':
        cycle = [
            'k',
            # sns.color_palette('deep')
            (0.2980392156862745, 0.4470588235294118, 0.6901960784313725),
            (0.8666666666666667, 0.5176470588235295, 0.3215686274509804),
            (0.3333333333333333, 0.6588235294117647, 0.40784313725490196),
            (0.7686274509803922, 0.3058823529411765, 0.3215686274509804),
            (0.5058823529411764, 0.4470588235294118, 0.7019607843137254),
            (0.5764705882352941, 0.47058823529411764, 0.3764705882352941),
            (0.8549019607843137, 0.5450980392156862, 0.7647058823529411),
            (0.5490196078431373, 0.5490196078431373, 0.5490196078431373),
            (0.8, 0.7254901960784313, 0.4549019607843137),
            (0.39215686274509803, 0.7098039215686275, 0.803921568627451),
            # sns.color_palette('dark')
            (0.0, 0.10980392156862745, 0.4980392156862745),
            (0.6941176470588235, 0.25098039215686274, 0.050980392156862744),
            (0.07058823529411765, 0.44313725490196076, 0.10980392156862745),
            (0.5490196078431373, 0.03137254901960784, 0.0),
            (0.34901960784313724, 0.11764705882352941, 0.44313725490196076),
            (0.34901960784313724, 0.1843137254901961, 0.050980392156862744),
            (0.6352941176470588, 0.20784313725490197, 0.5098039215686274),
            (0.23529411764705882, 0.23529411764705882, 0.23529411764705882),
            (0.7215686274509804, 0.5215686274509804, 0.0392156862745098),
            (0.0, 0.38823529411764707, 0.4549019607843137),
        ]
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(
        color=cycle
    )
    return

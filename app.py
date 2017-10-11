from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager
import os


def moving_average(a, n=3):
    """
    Calculates moving average in list.
    :param a:
    :param n:
    :return:
    """
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def plot_data(xticks,
              time,
              wav_data_avg,
              foreground_color,
              background_color,
              font_size_sub,
              font_size_lead,
              lead_text,
              sub_text,
              dpi_print):
    """
    Prints and/or plots soundwave image.
    :param xticks:
    :param time:
    :param wav_data_avg:
    :param foreground_color:
    :param background_color:
    :param font_size_sub:
    :param font_size_lead:
    :param lead_text:
    :param sub_text:
    :param dpi_print:
    :return:
    """

    matplotlib.rcParams['lines.linewidth'] = 0.007 # for 1000 dpi: 0.004
    matplotlib.rcParams['figure.dpi'] = 300
    matplotlib.rcParams['savefig.dpi'] = dpi_print
    # Allow for for more points to be drawn.
    matplotlib.rcParams['agg.path.chunksize'] = 10000
    matplotlib.rcParams['savefig.facecolor'] = background_color
    matplotlib.rcParams['savefig.edgecolor'] = foreground_color

    # A3: 297x420
    figure = plt.figure(figsize=(42 * 0.393701, 29.7 * 0.393701),
                        facecolor=background_color,
                        edgecolor=foreground_color)

    rect = figure.patch

    # Plot soundwave.
    plt.subplot(111).set_xticks(xticks)
    plt.axis('off')

    # Define and add text.
    font_sub = {'family': 'Laksaman',
                'color': foreground_color,
                'weight': 'normal',
                'size': font_size_sub}
    font_lead = {'family': 'Laksaman',
                 'color': foreground_color,
                 'weight': 'bold',
                 'size': font_size_lead}

    plt.figtext(0.5, 0.235, sub_text, fontdict=font_sub, horizontalalignment='center')
    plt.figtext(0.5, 0.185, lead_text, fontdict=font_lead, horizontalalignment='center')

    plt.subplots_adjust(left=0, bottom=0.305, right=1, top=0.895, wspace=0, hspace=0)
    plt.plot(time, wav_data_avg, color=foreground_color, rasterized=True)

    plt.savefig('output/soundwave.pdf',
                facecolor=background_color,
                edgecolor=foreground_color,
                transparent=True,
                papertype='a3',
                format='pdf')

    # plt.show()
    plt.close(figure)


def run(filename,
        background_color,
        foreground_color,
        lead_text,
        sub_text,
        font_size_lead,
        font_size_sub,
        dpi_print,
        generate_wav):
    """
    Generate soundwave.pdf.
    :param filename:
    :param background_color:
    :param foreground_color:
    :param lead_text:
    :param sub_text:
    :param font_size_lead:
    :param font_size_sub:
    :param dpi_print:
    :param generate_wav:
    :return:
    """
    # Convert .mp3 to .wav, if output/wav.wav doesn't exist yet.
    if generate_wav or not os.path.isfile("output/wav.wav"):
        sound = AudioSegment.from_mp3(filename)
        sound.export("output/wav.wav", format="wav")

    # Preprocess .wav data.
    f = wave.open("output/wav.wav", "rb")

    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]

    str_data = f.readframes(nframes)
    f.close()

    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    time = np.arange(0, nframes) * (1.0 / framerate)

    duration = nframes / float(framerate)
    xticks = np.arange(0, duration, 2)

    # Calculate avg. of channel values.
    # n_window = 50
    wave_data_avg = (wave_data[0] + wave_data[1]) / 2
    print(len(wave_data[0]))
    print(len(wave_data[1]))
    print(len(wave_data_avg))
    print(len(time))
    # Plot sound data.
    plot_data(xticks=xticks,
              time=time, #time[:len(time) - n_window + 1],
              wav_data_avg=wave_data[0],
              background_color=background_color,
              foreground_color=foreground_color,
              lead_text=lead_text,
              sub_text=sub_text,
              font_size_sub=font_size_sub,
              font_size_lead=font_size_lead,
              dpi_print=dpi_print)

# Generate sound wave image.
# Mounika. - Cut My Hair (feat. Cavetown)
# Wolf_Larsen_-_If_I_Be_Wrong
# CLAUDE DEBUSSY -  CLAIR DE LUNE
# Una Palabra
# Dinah Washington And Max Richter/This Bitter Earth And On The Nature Of Daylight.mp3
# Max Richter - The Blue Notebooks.mp3
# Sunshine Soundtrack ~ Surface of the Sun ~ Film Version ~ High Definition Audio
# György Ligeti - Lux Aeterna
# Lux Aeterna By Clint Mansell
# Daughter - Youth
run(filename="/home/raphael/Music/Neu/Daughter - Youth.mp3",
    background_color="red",
    foreground_color="white",
    lead_text="Y  O  U  T  H",
    sub_text="D A U G H T E R",
    font_size_lead=27,
    font_size_sub=23,
    dpi_print=1000,
    generate_wav=True)

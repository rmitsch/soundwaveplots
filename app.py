from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def plot_data(xticks,
              time,
              wav_data_avg,
              foreground_color,
              background_color,
              font_size_sub,
              font_size_lead):

    # Allow for for more points to be drawn.
    matplotlib.rcParams['agg.path.chunksize'] = 10000

    figure = plt.gcf()  # get current figure
    # A3: 297x420
    figure.set_size_inches(29.7 * 0.393701, 21 * 0.393701)

    rect = figure.patch
    rect.set_facecolor(background_color)

    # Plot soundwave.
    plt.subplot(111).set_xticks(xticks)
    plt.axis('off')

    plt.subplots_adjust(left=0, bottom=0.275, right=1, top=0.875, wspace=0, hspace=0)
    plt.plot(time, wav_data_avg, color=foreground_color, linewidth=0.0075, alpha=1)

    # Define and add text.
    font_sub = {'family': 'Laksaman',
                'color': foreground_color,
                'weight': 'normal',
                'size': font_size_sub}
    font_lead = {'family': 'Laksaman',
                 'color': foreground_color,
                 'weight': 'bold',
                 'size': font_size_lead}

    plt.figtext(0.5, 0.155, r'SLYTHERIN SUCKS', fontdict=font_sub, horizontalalignment='center')
    plt.figtext(0.5, 0.12, r'R A V E N C L A W  I S  A W E S O M E', fontdict=font_lead, horizontalalignment='center')

    plt.savefig('output/soundwave.pdf',
                dpi=300,
                facecolor=background_color,
                edgecolor=foreground_color,
                papertype='a3',
                format='pdf')

    plt.show()
    plt.close(figure)


def run():
    # # Print available fonts.
    # flist = matplotlib.font_manager.get_fontconfig_fonts()
    # names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
    # # Print available fonts.
    # for name in sorted(names):
    #     print(name)

    # Convert .mp3 to .wav.
    # sound = AudioSegment.from_mp3("/home/raphael/Music/Download/ThinkPinkR_The Cinematic Orchestra Arrival of the Birds & Transformation.mp3")
    # sound.export("output/wav.wav", format="wav")

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
    n_window = 50
    wav_data_avg = (wave_data[0] + wave_data[1]) / 2

    # Plot sound data.
    plot_data(xticks=xticks,
              time=time, #time[:len(time) - n_window + 1],
              wav_data_avg=wav_data_avg,
              background_color='red',
              foreground_color='white',
              font_size_sub=12,
              font_size_lead=14)

# Generate sound wave image.
run()
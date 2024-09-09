import numpy as np
# from scipy import signal
from scipy.fft import rfft, rfftfreq
from scipy.signal import spectrogram, butter, lfilter, freqz


class FrequencyAnalysis:

    @staticmethod
    def calc_fft(data, sample_rate, norm=None):
        """Calculate FFT. Transfrom Signal data from
        Time domain to Frequenct domain.

        Args:
            data (numpy.ndarray): Signal data in Time domain
            sample_rate (scalar): Sampling rate [Hz]

        Returns:
            1. numpy.ndarray: x-axis value: frequency
            2. numpy.ndarray: y-axis value: magnitude
        """
        sample_size = len(data)

        # yf = fft(data)
        # xf = fftfreq(sample_size, 1 / sample_rate)

        yf = rfft(data, norm=norm)  # only get the right side
        # yf = rfft(data, norm='forward')  # norm='forward' 'ortho'

        # as used rfft, need to use to rfftfreq to map
        xf = rfftfreq(sample_size, 1 / sample_rate)

        # How to plot:
        # plt.plot(xf, np.abs(yf))
        # plt.show()
        return xf, np.abs(yf)

    @staticmethod
    def calc_spectogram(data, sample_rate):
        f, t, Sxx = spectrogram(data, sample_rate)

        # How to plot:
        # fig, ax = plt.subplots()
        # spectro = ax.pcolormesh(t, f, Sxx, shading='gouraud')
        # fig.colorbar(spectro, label='|FFT Amplitude|')
        # ax.set_ylabel('Frequency [Hz]')
        # ax.set_xlabel('Time [sec]')
        # plt.show()
        return f, t, Sxx

    # == FILTER == #

    # == Bandpass Filter == #

    @staticmethod
    def bandpass_butter(lowcut, highcut, fs, order=5):
        return butter(order, [lowcut, highcut], fs=fs, btype='band')

    def bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.bandpass_butter(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # == Lowpass Filter == #

    @staticmethod
    def lowpass_butter(cutoff, fs, order=5):
        return butter(order, cutoff, fs=fs, btype='low', analog=False)

    def lowpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.lowpass_butter(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # == Visualize the Bandpass Filter == #

    def plot_bandpass_butter(self, lowcut, highcut, fs, order, worN=8000):

        b, a = self.bandpass_butter(lowcut, highcut, fs, order)
        w, h = freqz(b, a, fs=fs, worN=worN)

        # How to plot:
        # plt.plot(w, abs(h))
        # plt.show()
        return w, abs(h)

    # == Visualize the Lowpass Filter == #

    def plot_lowpass_butter(self, cutoff, fs, order, worN=8000):

        b, a = self.lowpass_butter(cutoff, fs, order)
        w, h = freqz(b, a, fs=fs, worN=worN)

        # How to plot:
        # plt.plot(w, abs(h))
        # plt.show()
        return w, abs(h)

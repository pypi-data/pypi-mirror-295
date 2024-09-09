import numpy as np
import scipy.stats as stat


class Stat:

    @staticmethod
    def mean_value(s):
        return np.mean(s)

    @staticmethod
    def std_value(s):
        return np.std(s)

    @staticmethod
    def rms_value(s):
        return np.sqrt(np.mean(s**2))

    @staticmethod
    def skew_value(s):
        return stat.skew(s)

    @staticmethod
    def kurtosis_value(s):
        return stat.kurtosis(s)

    @staticmethod
    def crest_value(s):
        return np.abs(s).max()/np.sqrt(np.mean(s**2))

    @staticmethod
    def clearance_value(s):
        return np.abs(s).max()/np.mean(np.sqrt(np.abs(s)))**2

    @staticmethod
    def shape_value(s):
        return np.sqrt(np.mean(s**2))/np.mean(np.abs(s))

    @staticmethod
    def impulse_value(s):
        return np.abs(s).max()/np.mean(np.abs(s))


class SignalCalculator(Stat):

    def __init__(self, data: np.ndarray, **kwargs):
        """ Calculate the sliding value of a signal
            with the window and step

        Args:
            data (np.ndarray): 1d
            window (int, optional): default =1
            step (int, optional): default =1
        """
        window = kwargs.get('window', 1)
        step = kwargs.get('step', 1)
        # sliding data
        self.data = self.sliding(data, window, step)

    @staticmethod
    def sliding(data, window, step):
        return np.lib.stride_tricks.sliding_window_view(data, window)[::step, :]

    def mean_sliding(self):
        return np.mean(self.data, axis=-1)  # axis=-1 means the last dimension

    def std_sliding(self):
        return np.std(self.data, axis=-1)

    def rms_sliding(self):
        return np.apply_along_axis(self.rms_value, -1, self.data)

    def skew_sliding(self):
        return np.apply_along_axis(self.skew_value, -1, self.data)

    def kurtosis_sliding(self):
        return np.apply_along_axis(self.kurtosis_value, -1, self.data)

    def crest_sliding(self):
        return np.apply_along_axis(self.crest_value, -1, self.data)

    def clearance_sliding(self):
        return np.apply_along_axis(self.clearance_value, -1, self.data)

    def shape_sliding(self):
        return np.apply_along_axis(self.shape_value, -1, self.data)

    def impulse_sliding(self):
        return np.apply_along_axis(self.impulse_value, -1, self.data)

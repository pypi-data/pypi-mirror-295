# Python libraries
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Own libraries
from .load import Load


class LockInAmplifier(Load):
    def __init__(self, lockin_delay_ch, lockin_x_ch, lockin_y_ch, history_number=None):
        super().__init__()
        # Channel names for Lock-In
        self.lockin_delay_ch = lockin_delay_ch
        self.lockin_x_ch = lockin_x_ch
        self.lockin_y_ch = lockin_y_ch
        # Only relevant if there are multiple recordings in one hdf5 file
        if history_number is None:
            self.history_number = "000"
        else:
            self.history_number = history_number

    def extract_lockin_data(self, f):
        time = np.array(
            f[f"{self.history_number}/{self.dev_name}/demods/{self.demod_ch}/{self.lockin_delay_ch}/timestamp"][:],
            dtype=np.float)
        # The timestamp has as a datatype uint64. If dataloss occurs, the timestamp is set to zero.
        # We convert the integers to float, so that we can set these areas with data loss to np.nan
        if self.debug:
            print(f"Detected {len(np.where(time == 0)[0])} data losses in lock-in data"
                  f"(missing timestamps get replaced by np.nan")
        time[np.where(time == 0)[0]] = np.nan
        if self.dev_name == "dev5138":
            time = (time - time[0]) * (1 / 60e6)  # The timestamp is in counts of the internal clock (60 MHz)
        elif self.dev_name == "dev2275":
            time = (time - time[0]) * (1 / 1.8e9)  # The timestamp is in counts of the internal clock (1.8 GHz)
        else:
            raise NameError("Couldn't detect Lock-In name in measurement file. Neither 'dev5138' nor 'dev2275'")
        delay = f[f"{self.history_number}/{self.dev_name}/demods/{self.demod_ch}/{self.lockin_delay_ch}/value"][:]
        signal_x = f[f"{self.history_number}/{self.dev_name}/demods/{self.demod_ch}/{self.lockin_x_ch}/value"][:]
        signal_y = f[f"{self.history_number}/{self.dev_name}/demods/{self.demod_ch}/{self.lockin_y_ch}/value"][:]
        if self.only_x:
            signal = signal_x - np.mean(signal_x)
        else:
            ang = self._minimize_y_lockin(signal_x, signal_y)
            X = signal_x * np.cos(-ang) - signal_y * np.sin(-ang)
            # Y = signal_x * np.sin(-ang) + signal_y * np.cos(-ang)
            signal = X
        return time, delay, signal

    def _read_lockin_attributes(self, f):
        self.history_traces = list(f.keys())
        self.dev_name = list(f[self.history_traces[0]].keys())[0]
        self.demod_ch = list(f[f"{self.history_traces[0]}/{self.dev_name}/demods"].keys())[0]


class DewesoftDAQ(Load):
    def __init__(self, lock_in_to_dewesoft, dewesoft_signal_X, dewesoft_signal_Y, file_name, dewesoft_signal_ch=None):
        super().__init__(file_name)
        if lock_in_to_dewesoft:
            # For lock-in record with two channels:
            self.dewesoft_signal_X = dewesoft_signal_X
            self.dewesoft_signal_Y = dewesoft_signal_Y
        else:
            self.dewesoft_signal_ch = dewesoft_signal_ch


class Oscilloscope(Load):
    def __init__(self, file_name):
        super().__init__(file_name)


class Picoscope(Load):
    def __init__(self, file_name):
        super().__init__(file_name)

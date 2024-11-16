"""
Python script for natHacks 2024 project!
Start date: Nov 14, 2024
End date:

Authors:
Sabrina 
Tazmeen
Percy
Amna
Jassica
"""

"""

import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt

# brain wave ranges (in Hz) - (start, end)
delta = (0.5, 4)
theta = (4, 8)
alpha = (8, 12)
beta = (12, 30)
gamma = (30, 100)

brain_wave_readings = {delta:0, theta:0, alpha:0, beta:0, gamma:0} #brain wave readings

params = BrainFlowInputParams()
params.serial_port = 'COM6' #Change this depending on your device and OS
board_id = 38 #Change this depending on your device

#Prepares the board for reading data
board = BoardShim(BoardIds.MUSE_2_BOARD.value, params)
board.prepare_session()

board.start_stream()
time.sleep(5)

data = board.get_board_data()
eeg_channels = BoardShim.get_eeg_channels(BoardIds.MUSE_2_BOARD.value)
sampling_rate = BoardShim.get_sampling_rate(BoardIds.MUSE_2_BOARD.value)

# isolate the eeg channels
eeg_channels = board.get_eeg_channels(board_id)
eeg_data = data[eeg_channels]

print(eeg_channels)
print(eeg_data.shape)

# Perform Fast Fourier Transform (FFT)
fft_list = []
for channel in eeg_data:
    fft_result = np.fft.fft(channel)
    fft_magnitude = np.abs(fft_result)  # Magnitude of the FFT
    frequencies = np.fft.fftfreq(len(fft_result), 1 / sampling_rate)
    fft_list.append(frequencies)

# Plot the frequency spectrum
plt.title("Frequency Spectrum of EEG Data (TP9)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.show()

board.stop_stream()
# Releases the board session
board.release_session()

"""
import argparse
import time
import brainflow
import numpy as np

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowOperations, DetrendOperations

# # use synthetic board for demo
params = BrainFlowInputParams()
# board_id = BoardIds.SYNTHETIC_BOARD.value
board_id = 38 #id for Muse 2
sampling_rate = BoardShim.get_sampling_rate(board_id)
nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
board = BoardShim(board_id, params)
# board.prepare_session()
# board.start_stream()
# time.sleep(60)
# data = board.get_board_data()
data = DataFilter.read_file('eeg_data_test_2.csv') #Reads file back
# board.stop_stream()
# board.release_session()
eeg_channels = BoardShim.get_eeg_channels(board_id)
# # use first eeg channel for demo
# # second channel of synthetic board is a sine wave at 10 Hz, should see big 'alpha'
eeg_channel = eeg_channels[1]

eeg_channels = range(len(data))
for eeg_channel in eeg_channels:

    # optional: detrend
    DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)

    psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate, WindowOperations.HANNING.value)
    plt.plot(psd[1][:100], psd[0][:100])
    plt.show()

# calc band power
# delta = DataFilter.get_band_power(psd, 0.5,4.0)
# theta = DataFilter.get_band_power(psd, 4.0,8.0)
# print("Delta/Theta Ratio is: %f" %(delta / theta))
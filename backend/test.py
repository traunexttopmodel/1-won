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
# nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
board = BoardShim(board_id, params)
board.prepare_session()
board.start_stream()
time.sleep(5)
data = board.get_board_data()
# data = DataFilter.read_file('eeg_data_test_3.csv') #Reads file back
board.stop_stream()
board.release_session()
eeg_channels = BoardShim.get_eeg_channels(board_id)
# # use first eeg channel for demo
# # second channel of synthetic board is a sine wave at 10 Hz, should see big 'alpha'

eeg_channel = range(len(eeg_channels))
for eeg_channel in eeg_channels:

    # optional: detrend
    #DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
    DataFilter.perform_bandstop(
                                data[eeg_channel], #data
                                sampling_rate, #sampling rate
                                55, #start freq
                                65, #end freq
                                1, #order
                                FilterTypes.BUTTERWORTH, #filter type
                                2 #ripple
                                )
    
    DataFilter.perform_bandstop(
                                data[eeg_channel], #data
                                sampling_rate, #sampling rate
                                0, #start freq
                                5, #end freq
                                1, #order
                                FilterTypes.BUTTERWORTH, #filter type
                                2 #ripple
                                )

    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
    psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate, WindowOperations.HANNING.value)
    plt.plot(psd[1][:60], psd[0][:60])
    plt.show()

# calc band power
delta = DataFilter.get_band_power(psd, 0.5,4.0)
theta = DataFilter.get_band_power(psd, 4.0,8.0)
print("Delta/Theta Ratio is: %f" %(delta / theta))
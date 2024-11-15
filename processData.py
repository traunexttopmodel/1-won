#--------------------------------------------------------------------------------
# SUMMARY: This function process the data by:
#          1) finding the Power Spectral Density (PSD) of each channel - shows the power of the signal in each frequency,
#          2) plot it,
#          3) find the average bandpower of each type of waves throughout the 4 channels,
#          4) find bandpower ratio between all combo,
#          5) and identify the dominant brain wave type (Gamma, Beta, Alpha, Theta, Delta)
#--------------------------------------------------------------------------------

import argparse
import time
import brainflow
import numpy as np

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowOperations, DetrendOperations

def processData(eeg_channels, eeg_data):

    # Setup
    board_id = 38
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)

    for eeg_channel in eeg_channels:
        # Find PSD of channel
        psd = DataFilter.get_psd_welch(eeg_data[eeg_channel], nfft, nfft // 2, sampling_rate, WindowOperations.HANNING.value)
        
        # Plot PSD of that channel
        plt.plot(psd[1][:60], psd[0][:60])
        plt.show()
#--------------------------------------------------------------------------------
# SUMMARY: This function process the data by:
#          1) finding the Power Spectral Density (PSD) of each channel - shows the power of the signal in each frequency,
#          2) plot it,
#          3) find the average bandpower (amount of activity in a frequency range) of each type of waves throughout the 4 channels,
#          4) find relative bandpowers to total bandpower,
#          5) and identify the dominant brain wave (Gamma, Beta, Alpha, Theta, Delta)
#          It returns the string of the dominant brain wave
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
    delta = theta = alpha = beta = gamma = total = 0

    for eeg_channel in eeg_channels:
        # Find PSD of channel
        psd = DataFilter.get_psd_welch(eeg_data[eeg_channel], nfft, nfft // 2, sampling_rate, WindowOperations.HANNING.value)
        
        # Plot PSD of that channel
        plt.plot(psd[1][:60], psd[0][:60])
        plt.show()

        # Sum up bandpower of each brain wave
        delta += DataFilter.get_band_power(psd, 0.5,4)
        theta += DataFilter.get_band_power(psd, 4,8)
        alpha += DataFilter.get_band_power(psd, 8,13)
        beta += DataFilter.get_band_power(psd, 13,35)
        gamma += DataFilter.get_band_power(psd, 35.0,100)
        total += DataFilter.get_band_power(psd, 0,100)
    
    # Find average bandpower of each brain wave 
    delta = delta/4
    theta = theta/4
    alpha = alpha/4
    beta = beta/4
    gamma = gamma/4
    total = total/4

    # Find relative bandpower of each
    relativeDelta = delta/total
    relativeTheta = theta/total
    relativeAlpha = alpha/total
    relativeBeta = beta/total
    relativeGamma = gamma/total
    relativeBandpowers = [relativeDelta, relativeTheta, relativeAlpha, relativeBeta, relativeGamma]

    # Find dominant brain wave (highest relative bandpower) & return
    highestRelativeBandpower = max(relativeBandpowers)
    if (highestRelativeBandpower == relativeDelta): return "Delta"
    if (highestRelativeBandpower == relativeTheta): return "Theta"
    if (highestRelativeBandpower == relativeAlpha): return "Alpha"
    if (highestRelativeBandpower == relativeBeta): return "Beta"
    if (highestRelativeBandpower == relativeGamma): return "Gamma"
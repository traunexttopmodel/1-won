#--------------------------------------------------------------------------------
# SUMMARY: This function process the data by:
#          1) finding the Power Spectral Density (PSD) of each channel - shows the power of the signal in each frequency,
#          2) smooth it out using Gaussian smoothing to reduce glitches and imitate analog data
#          3) find the average bandpower (amount of activity in a frequency range) of each type of waves
#             throughout channels 1, 2 and 3 (exlcuding channel 0),
#          4) find the Theta/Beta, Alpha/Theta ratio and return
#           
# NOTES: 
#          * The commented out portion of the program can be uncommented to see the 
#            smoothed graphs and dominant brainwave 
#
#          * Theta/Beta and Alpha/Theta ratios were chosen to allow simplified categorization of 
#            mild and severe warning, as relative bandpowers often result in Delta/Theta as the dominant brainwave 
#            and does not allow for data nuances -
#            (dominating Delta/Theta does not automatically equate to fatigue, 
#            eg. a mildly tired person could have strong Beta/Alpha brainwaves but still stronger Theta signals.
#            Therefore, must compare in relative to other bandpowers to gain a more accurate diagnosis).
#            An example of studies using Theta/Beta Ratio: https://pmc.ncbi.nlm.nih.gov/articles/PMC7391399/
#--------------------------------------------------------------------------------

import brainflow
import matplotlib.pyplot as plt
import numpy as np

from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter, WindowOperations
from scipy.ndimage import gaussian_filter


def processData(eeg_channels, eeg_data):

    # Setup
    board_id = 38
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    nfft = DataFilter.get_nearest_power_of_two(150)
    delta = theta = alpha = beta = gamma = total = 0
    psd_threshold = 20000

    # psd_list = []
    # smoothed_psd_list = []

    for eeg_channel in range(1,len(eeg_channels)):
        # Find PSD of channel
        psd = DataFilter.get_psd_welch(eeg_data[eeg_channel], nfft, nfft // 2, sampling_rate, WindowOperations.HANNING.value)
        psd = filter_high_psd(psd, psd_threshold)
        smoothed_psd = smooth_psd(psd, sigma=3)

        # # Save for plotting
        # psd_list.append(psd)
        # smoothed_psd_list.append(smoothed_psd)

        # Ensure that the frequency ranges are valid for your PSD data
        try:
            delta += DataFilter.get_band_power(smoothed_psd, 0.5, 4)
            theta += DataFilter.get_band_power(smoothed_psd, 4, 8)
            alpha += DataFilter.get_band_power(smoothed_psd, 8, 13)
            beta += DataFilter.get_band_power(smoothed_psd, 13, 35)
            gamma += DataFilter.get_band_power(smoothed_psd, 35, 100)
            total += DataFilter.get_band_power(smoothed_psd, 0, 100)
        except brainflow.BrainFlowError as e:
            print(f"Error in band power calculation for channel {eeg_channel}: {e}")
    
    #plot_psd_comparison(eeg_channels[1:], psd_list, smoothed_psd_list)
    
    # Find average bandpower of each brain wave 
    delta = delta/4
    theta = theta/4
    alpha = alpha/4
    beta = beta/4
    gamma = gamma/4
    total = total/4

    # Find relative bandpower of each
    # relativeDelta = delta/total
    # relativeTheta = theta/total
    # relativeAlpha = alpha/total
    # relativeBeta = beta/total
    # relativeGamma = gamma/total
    # relativeBandpowers = [relativeDelta, relativeTheta, relativeAlpha, relativeBeta, relativeGamma]
    #print(relativeBandpowers)

    thetaBetaRatio = theta/beta
    alphaThetaRation = alpha/theta

    # Find dominant brain wave (highest relative bandpower) & return
    # highestRelativeBandpower = max(relativeBandpowers)
    # if (highestRelativeBandpower == relativeDelta): return "Delta", thetaBetaRatio, thetaAlphaRatio
    # if (highestRelativeBandpower == relativeTheta): return "Theta", thetaBetaRatio, thetaAlphaRatio
    # if (highestRelativeBandpower == relativeAlpha): return "Alpha", thetaBetaRatio, thetaAlphaRatio
    # if (highestRelativeBandpower == relativeBeta): return "Beta", thetaBetaRatio, thetaAlphaRatio
    # if (highestRelativeBandpower == relativeGamma): return "Gamma", thetaBetaRatio, thetaAlphaRatio

    return thetaBetaRatio, alphaThetaRation







def smooth_psd(psd, sigma=2):

    # Extract PSD values and frequencies from the input tuple
    psd_values = psd[0]
    frequencies = psd[1]

    # Apply Gaussian filter to smooth the PSD values
    smoothed_psd_values = gaussian_filter(psd_values, sigma=sigma)
    smoothed_psd = (smoothed_psd_values, frequencies)

    return smoothed_psd




def filter_high_psd(psd, threshold):

    psd_values = psd[0]
    frequency = psd[1]

    psd_values = np.where(psd_values > threshold, 0, psd_values)
    return (psd_values,frequency)  # Replace values above threshold with 0




def plot_psd_comparison(eeg_channels, psd_list, smoothed_psd_list):
    
    num_channels = len(eeg_channels)
    fig, axs = plt.subplots(1, num_channels, figsize=(15, 5), sharey=True)
    
    for i, eeg_channel in enumerate(eeg_channels):
        psd = psd_list[i]
        smoothed_psd = smoothed_psd_list[i]
        
        axs[i].plot(psd[1], psd[0], label='Original PSD', color='blue', alpha=0.7)
        axs[i].plot(smoothed_psd[1], smoothed_psd[0], label='Smoothed PSD', color='red', linewidth=2)
        axs[i].set_xlim([0, 60])  # Limit x-axis to 60 Hz
        axs[i].set_xlabel('Frequency (Hz)')
        axs[i].set_title(f'Channel {eeg_channel}')
        axs[i].grid(True)
        
        if i == 0:
            axs[i].set_ylabel('Power Spectral Density')
    
    fig.suptitle('Original vs Smoothed PSD for EEG Channels', fontsize=16)
    #fig.legend(loc='upper center', ncol=2)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
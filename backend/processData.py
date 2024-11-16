#--------------------------------------------------------------------------------
# SUMMARY: This function process the data by:
#          1) finding the Power Spectral Density (PSD) of each channel - shows the power of the signal in each frequency,
#          2) plot it,
#          3) find the average bandpower (amount of activity in a frequency range) of each type of waves throughout the 4 channels,
#          4) find relative bandpowers to total bandpower,
#          5) and identify the dominant brain wave (Gamma, Beta, Alpha, Theta, Delta)
#          It returns the string of the dominant brain wave
#--------------------------------------------------------------------------------

import brainflow
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter, WindowOperations
from scipy.ndimage import gaussian_filter

def processData(eeg_channels, eeg_data):

    # Setup
    board_id = 38
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    nfft = DataFilter.get_nearest_power_of_two(150)
    delta = theta = alpha = beta = gamma = total = 0

    for eeg_channel in eeg_channels:
        # Find PSD of channel
        psd = DataFilter.get_psd_welch(eeg_data[eeg_channel], nfft, nfft // 2, sampling_rate, WindowOperations.HANNING.value)
        smoothed_psd = smooth_psd(psd, sigma=3)

        # Plot PSD of that channel
        # plt.plot(psd[1][:50], psd[0][:50])
        # plt.show()
        # plt.xlabel("Frequency")
        # plt.ylabel("Power Spectral")

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

    thetaBetaRatio = theta/beta

    # Find dominant brain wave (highest relative bandpower) & return
    highestRelativeBandpower = max(relativeBandpowers)
    if (highestRelativeBandpower == relativeDelta): return "Delta", thetaBetaRatio
    if (highestRelativeBandpower == relativeTheta): return "Theta", thetaBetaRatio
    if (highestRelativeBandpower == relativeAlpha): return "Alpha", thetaBetaRatio
    if (highestRelativeBandpower == relativeBeta): return "Beta", thetaBetaRatio
    if (highestRelativeBandpower == relativeGamma): return "Gamma", thetaBetaRatio







def smooth_psd(psd, sigma=2):
    """
    Apply Gaussian smoothing to the PSD data.
    
    Args:
        psd (tuple): A tuple containing the PSD power values and corresponding frequency bins.
        sigma (float): The standard deviation for the Gaussian filter (controls smoothing).
        
    Returns:
        smoothed_psd (numpy array): The smoothed PSD data.
    """
    # Extract PSD values and frequencies from the input tuple
    psd_values = psd[0]
    frequencies = psd[1]

    # Apply Gaussian filter to smooth the PSD values
    smoothed_psd_values = gaussian_filter(psd_values, sigma=sigma)
    smoothed_psd = (smoothed_psd_values, frequencies)
    
    # Plot original and smoothed PSD for comparison
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, psd_values, label='Original PSD', color='blue', alpha=0.7)
    plt.plot(frequencies, smoothed_psd_values, label='Smoothed PSD', color='red', linewidth=2)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power Spectral Density')
    plt.title('Original vs Smoothed PSD')
    plt.legend()
    plt.grid(True)
    plt.show()

    return smoothed_psd
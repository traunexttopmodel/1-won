from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
import time

board_id = 38

#------------------------------------------ GET DATA ---------------------------------------------------

eeg_data = DataFilter.read_file('eeg_data_test_5.csv') #Reads file back
print(eeg_data.shape)

#------------------------------------------ PREPROCESS DATA ---------------------------------------------------

for i in range(0,4):
    #Plot EEG channels
    plt.plot(np.arange(eeg_data.shape[1]), eeg_data[i])
    plt.title("Raw EEG Data")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.show()

# Define brainwave frequency bands
delta_band = (0.5, 4)
theta_band = (4, 8)
alpha_band = (8, 13)
beta_band = (13, 32)
gamma_band = (32, 100)

bands = {"Delta": delta_band, "Theta": theta_band, "Alpha": alpha_band, "Beta": beta_band, "Gamma": gamma_band}

#------------------------------------------ ANALYZE DATA ---------------------------------------------------

# Sampling rate for Muse 2 board
sampling_rate = BoardShim.get_sampling_rate(board_id)

# Analyze each EEG channel
for i, channel_data in enumerate(eeg_data):
    # Perform FFT
    fft_result = np.fft.fft(channel_data)
    fft_magnitude = np.abs(fft_result)  # Magnitude of the FFT
    frequencies = np.fft.fftfreq(len(fft_magnitude), 1 / sampling_rate)
    
    # Only keep positive frequencies - why?
    positive_freqs = frequencies[:len(frequencies) // 2]
    positive_magnitude = fft_magnitude[:len(fft_magnitude) // 2]
    
    # Calculate power in each band
    band_powers = {}
    for band_name, (low, high) in bands.items():
        # Find indices for the frequency band
        band_indices = np.where((positive_freqs >= low) & (positive_freqs <= high))
        band_power = np.sum(positive_magnitude[band_indices] ** 2)  # Sum of squared magnitudes
        band_powers[band_name] = band_power

    # Determine the dominant brainwave
    dominant_band = max(band_powers, key=band_powers.get)
    print(f"Channel {i + 1}: Dominant brainwave = {dominant_band}, Power = {band_powers[dominant_band]:.2f}")

    # Plot the FFT for visualization
    plt.plot(positive_freqs, positive_magnitude)
    plt.title(f"Frequency Spectrum of EEG Data (Channel {i + 1})")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()

#------------------------------------------ SAVE DATA ---------------------------------------------------

# print(eeg_data.shape)
# DataFilter.write_file(eeg_data, 'eeg_data_test.csv', 'w') #Writes into a csv file in the current directory

# restored_data = DataFilter.read_file('eeg_data_test.csv') #Reads file back
# print(restored_data.shape)

# #This shows how much the saved data differs from the original data, they are very similar but not equal.
# print(eeg_data - restored_data)
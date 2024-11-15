from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
import time

params = BrainFlowInputParams()
params.serial_port = 'COM6' #Change this depending on your device and OS
board_id = 38 #Change this depending on your device

#Prepares the board for reading data
try:
    board_id = 38
    board = BoardShim(board_id, params)
    board.prepare_session()
    print("Successfully prepared physical board.")
except Exception as e:
    print(e)
    #If the device cannot be found or is being used elsewhere, creates a synthetic board instead
    print("Device could not be found or is being used by another program, creating synthetic board.")
    board_id = BoardIds.SYNTHETIC_BOARD
    board = BoardShim(board_id, params)
    board.prepare_session()
#Releases the board session
board.release_session()

#------------------------------------------ GET DATA ---------------------------------------------------

#read data
print("Starting Stream")
board.prepare_session()
board.start_stream()
time.sleep(5) #wait 5 seconds
data = board.get_board_data() #gets all data from board and removes it from internal buffer
print("Ending stream")
board.stop_stream()
board.release_session()

#We want to isolate just the eeg data
eeg_channels = board.get_eeg_channels(board_id)
#print(eeg_channels)
eeg_data = data[eeg_channels]
#print(eeg_data.shape)

#------------------------------------------ PREPROCESS DATA ---------------------------------------------------

#Plot the first EEG channel
plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])
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

# Perform FFT
sampling_rate = BoardShim.get_sampling_rate(board_id)
fft_result = np.fft.fft(eeg_data)
frequencies = np.fft.fftfreq(len(fft_result), d=1/sampling_rate)
magnitude = np.abs(fft_result)

# Calculate power in each band
def band_power(frequencies, magnitudes, band):
    indices = np.where((frequencies >= band[0]) & (frequencies <= band[1]))
    return np.sum(magnitudes[indices])

delta_power = band_power(frequencies, magnitude, delta_band)
theta_power = band_power(frequencies, magnitude, theta_band)
alpha_power = band_power(frequencies, magnitude, alpha_band)
beta_power = band_power(frequencies, magnitude, beta_band)
gamma_power = band_power(frequencies, magnitude, gamma_band)

# Identify the dominant brainwave type
power_levels = {
    'Delta': delta_power,
    'Theta': theta_power,
    'Alpha': alpha_power,
    'Beta': beta_power,
    'Gamma': gamma_power
}

dominant_brainwave = max(power_levels, key=power_levels.get)

print("Power Levels:", power_levels)
print("Dominant Brainwave:", dominant_brainwave)
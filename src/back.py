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

params = BrainFlowInputParams()

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
plt.plot(positive_freqs, positive_magnitude)
plt.title("Frequency Spectrum of EEG Data (TP9)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.show()

board.stop_stream()
# Releases the board session
board.release_session()




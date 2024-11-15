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

"""
try:
    board_id = -1
    board = BoardShim(board_id, params)
    board.prepare_session()
    print("Successfully prepared physical board.")
except Exception as e:
    print(e)
    # If the device cannot be found or is being used elsewhere, creates a synthetic board instead
    print("Device could not be found or is being used by another program, creating synthetic board.")
    board_id = BoardIds.SYNTHETIC_BOARD
    board = BoardShim(board_id, params)
    board.prepare_session()
"""

params = BrainFlowInputParams()

board = BoardShim(BoardIds.MUSE_2_BOARD.value, params)
board.prepare_session()

board.start_stream()
time.sleep(5)

data = board.get_board_data()

eeg_data = data[BoardShim.get_eeg_channels(BoardIds.MUSE_2_BOARD.value)[0]]
sampling_rate = BoardShim.get_sampling_rate(BoardIds.MUSE_2_BOARD.value)

# Perform Fast Fourier Transform (FFT)
fft_result = np.fft.fft(eeg_data)
fft_magnitude = np.abs(fft_result)  # Magnitude of the FFT
frequencies = np.fft.fftfreq(len(fft_result), 1 / sampling_rate)

# Only keep the positive frequencies
positive_freqs = frequencies[:len(frequencies) // 2]
positive_magnitude = fft_magnitude[:len(fft_magnitude) // 2]

# Plot the frequency spectrum
plt.plot(positive_freqs, positive_magnitude)
plt.title("Frequency Spectrum of EEG Data (TP9)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.show()

board.stop_stream()
# Releases the board session
board.release_session()




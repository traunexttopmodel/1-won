from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowOperations, DetrendOperations
import numpy as np
from scipy.signal import detrend
from nfft import nfft
import matplotlib.pyplot as plt
import time
import argparse
import pandas as pd
import statistics



params = BrainFlowInputParams()
params.serial_port = 'COM6' #Change this depending on your device and OS
board_id = 38 #Change this depending on your device
sampling_rate = BoardShim.get_sampling_rate(board_id)

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

nfft = DataFilter.get_nearest_power_of_two(sampling_rate)

#Releases the board session
board.release_session()




#------------------------------------------ GET DATA ---------------------------------------------------

#read data
# print("Starting Stream")
# board.prepare_session()
# board.start_stream()
# time.sleep(5) #wait 5 seconds
# data = board.get_board_data() #gets all data from board and removes it from internal buffer
data = DataFilter.read_file('eeg_data_test_6.csv') #Reads file back
board_id = 38
# print("Ending stream")
# board.stop_stream()
# board.release_session()

#We want to isolate just the eeg data
<<<<<<< HEAD
eeg_channels = board.get_eeg_channels(board_id)
print(eeg_channels)
eeg_data = data[eeg_channels]
EEG_channels=[0,1,2,3] 
# '''EEG channel codes [0,1,2,3]'''
=======
eeg_channels = BoardShim.get_eeg_channels(board_id)
# eeg_data = data[eeg_channels]
>>>>>>> d3f7e5ee93aa66399381854342279d310091268f
#print(eeg_data.shape)

#------------------------------------------ PREPROCESS DATA ---------------------------------------------------

#Plot the **first** EEG channel
plt.plot(np.arange(data.shape[1]), data[0])
plt.title("Raw EEG Data")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.show()


# ----------------------TRYING TO FILTER & SEE ALPHA/BETA----------------------

#Filter data - apply to each channel separately 
#filter to remove artifacts
# for channel in range(eeg_data.shape[0]): # applied to all channels??
#     DataFilter.perform_lowpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 50.0, 5,
#                                        FilterTypes.BUTTERWORTH, 1) #BUTTERWORTH is a lowpass/highpass filter with low phase distortion (caused by data omission)
#     DataFilter.perform_highpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 8.0, 4,
#                                         FilterTypes.BUTTERWORTH, 0)
# plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])
# plt.title("Filtered EEG Data")
# plt.show()
#plt.plot(x, y)
#here using NumPy library to create array of basically timestamps for all the eeg data points we collect (horizontal axis)



#Filter to count Alpha Waves ?
#def alpha():
# for channel in range(eeg_data.shape[0]): # all channels??
#         DataFilter.perform_bandpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 8.0, 13.0, 4, 
#                                            FilterTypes.BUTTERWORTH, 0) #ripple = 0. what is a ripple? how much oscillation 
#     plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])
#     plt.xlabel("Alpha")
#     plt.title("Filtered EEG Data: Alpha Waves")
#     plt.show()
#alpha()


#Filter to count Beta Waves ?
#def beta():
    # for channel in range(eeg_data.shape[0]): # applied to all channels
    #     DataFilter.perform_bandpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 13.0, 35.0, 4, 
    #                                        FilterTypes.BUTTERWORTH, 0) #ripple = 0. what is a ripple? how much oscillation 
    # plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])
    # plt.title("Filtered EEG Data: Beta Waves")
    # plt.show()
#beta()


#-------------------------------------CHANNEL GRAPHS-----------------------

for channel_idx in EEG_channels: #channel idx is indices for the different muse channels; channels 0-3 are the eeg channels
    DataFilter.detrend(data[channel_idx], DetrendOperations.LINEAR.value)
    psd0=DataFilter.get_psd_welch(data[channel_idx], nfft, nfft//2, sampling_rate, WindowOperations.HANNING.value)
    plt.plot(psd0[1][:60], psd0[0][:60])
    plt.title(f"Channel {channel_idx}")
    plt.show()





# eeg_channel0=eeg_channels[0]
# DataFilter.detrend(data[eeg_channel0], DetrendOperations.LINEAR.value)
# psd0=DataFilter.get_psd_welch(data[eeg_channel0], nfft, nfft//2, sampling_rate, WindowOperations.HANNING.value)
# plt.plot(psd0[1][:60], psd0[0][:60])
# plt.title("Channel 0")
# plt.show()

# eeg_channel1=eeg_channels[1]
# DataFilter.detrend(data[eeg_channel1], DetrendOperations.LINEAR.value)
# psd1=DataFilter.get_psd_welch(data[eeg_channel1], nfft, nfft//2, sampling_rate, WindowOperations.HANNING.value)
# plt.plot(psd1[1][:60], psd1[0][:60])
# plt.title("Channel 1")
# plt.show()

# eeg_channel2=eeg_channels[2]
# DataFilter.detrend(data[eeg_channel2], DetrendOperations.LINEAR.value)
# psd2=DataFilter.get_psd_welch(data[eeg_channel2], nfft, nfft//2, sampling_rate, WindowOperations.HANNING.value)
# plt.plot(psd2[1][:60], psd2[0][:60])
# plt.title("Channel 2")
# plt.show()

# eeg_channel3=eeg_channels[3]
# DataFilter.detrend(data[eeg_channel3], DetrendOperations.LINEAR.value)
# psd3=DataFilter.get_psd_welch(data[eeg_channel3], nfft, nfft//2, sampling_rate, WindowOperations.HANNING.value)
# plt.plot(psd3[1][:60], psd3[0][:60])
# plt.title("Channel 3")
# plt.show()



# delta=statistics.mean(
#     DataFilter.get_band_power(psd1, 0.5, 4.0),
#     DataFilter.get_band_power(psd2, 0.5, 4.0),
#     DataFilter.get_band_power(psd3, 0.5, 4.0),
#     DataFilter.get_band_power(psd4, 0.5, 4.0))



# theta= statistics.mean(    
#     DataFilter.get_band_power(psd1, 4.0, 8.0),
#     DataFilter.get_band_power(psd2, 4.0, 8.0),
#     DataFilter.get_band_power(psd3, 4.0, 8.0),
#     DataFilter.get_band_power(psd4, 4.0, 8.0))




bands = {
    "Delta": (0.5, 4.0),
    "Theta": (4.0, 8.0),
    "Alpha": (8.0, 13.0),
    "Beta": (13.0, 30.0)
}


def get_bandpowers_for_channel(eeg_data, channel_idx, bands):
    psd = DataFilter.get_psd(eeg_data[channel_idx], len(eeg_data[channel_idx]), 0)  # Compute PSD
    bandpowers = {}
    for band_name, (low, high) in bands.items():
        bandpower = DataFilter.get_band_power(psd, low, high)
        bandpowers[band_name] = bandpower
    return bandpowers

channel_bandpowers = {}
for channel_idx in EEG_channels:
    bandpowers = get_bandpowers_for_channel(eeg_data, channel_idx, bands)
    channel_bandpowers[channel_idx] = bandpowers

average_bandpowers = {band_name: 0.0 for band_name in bands}

for band_name in bands:
    total_bandpower = 0
    for channel_idx in EEG_channels:
        total_bandpower += channel_bandpowers[channel_idx][band_name]
    average_bandpowers[band_name] = total_bandpower / len(EEG_channels)


print("Delta:Theta Ratio is: %f" %((average_bandpowers[bands.Delta])/(average_bandpowers[bands.Theta])))



# Brainwave Type frequency bands
delta = (0.5, 4.0),
theta= (4.0, 8.0)
alpha_band = (8, 13)
beta_band = (13, 35)
gamma_band = (35, 100)

# Perform FFT
sampling_rate = BoardShim.get_sampling_rate(board_id)
fft_result = np.fft.fft(data)
frequencies = np.fft.fftfreq(len(fft_result), d=1/sampling_rate)
magnitude = np.abs(fft_result)

# Calculate power in each band
def band_power(frequencies, magnitudes, band):
    indices = np.where((frequencies >= band[0]) & (frequencies <= band[1]))
    return np.sum(magnitudes[indices])

#delta_power = band_power(frequencies, magnitude, delta_band)
#theta_power = band_power(frequencies, magnitude, theta_band)
alpha_power = band_power(frequencies, magnitude, alpha_band)
beta_power = band_power(frequencies, magnitude, beta_band)
gamma_power = band_power(frequencies, magnitude, gamma_band)

# Identify the dominant brainwave type
power_levels = {
    #'Delta': delta_power,
    #'Theta': theta_power,
    'Alpha': alpha_power,
    'Beta': beta_power,
    'Gamma': gamma_power
}

dominant_brainwave = max(power_levels, key=power_levels.get)

print("Power Levels:", power_levels)
print("Dominant Brainwave:", dominant_brainwave)
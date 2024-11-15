#--------------------------------------------------------------------------------
# SUMMARY: This function filters out the highs (~60Hz and ~0Hz spike) in EACH channel
#          and return cleaner EEG channels
#--------------------------------------------------------------------------------

from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter, FilterTypes

def preprocessData(eeg_channels, eeg_data):

    # Setup
    board_id = 38
    sampling_rate = BoardShim.get_sampling_rate(board_id)

    #----------------------- FILTER DATA FOR EACH CHANNEL ----------------------

    for eeg_channel in eeg_channels:
        # Filtering the spike at 60Hz
        DataFilter.perform_bandstop(
                                    eeg_data[eeg_channel], #data
                                    sampling_rate, #sampling rate
                                    55, #start freq
                                    65, #end freq
                                    1, #order
                                    FilterTypes.BUTTERWORTH, #filter type
                                    2 #ripple
                                    )
        
        # Filtering the spike at 0Hz
        DataFilter.perform_bandstop(
                                    eeg_data[eeg_channel], #data
                                    sampling_rate, #sampling rate
                                    0, #start freq
                                    5, #end freq
                                    1, #order
                                    FilterTypes.BUTTERWORTH, #filter type
                                    2 #ripple
                                    )
        
    #----------------------- RETURNING CLEANED DATA ----------------------
    return eeg_channels, eeg_data
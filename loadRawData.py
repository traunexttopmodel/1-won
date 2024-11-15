#--------------------------------------------------------------------------------
# SUMMARY: This function collect live data if no parameter passed, 
#          or load in CSV data if filename is passed.
#          It returns raw EEG dataset, unfiltered. (eeg_channels, eeg_data)
#--------------------------------------------------------------------------------


from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter
import time

def loadRawData(filename=None):

    # Setup
    params = BrainFlowInputParams()
    params.serial_port = 'COM6'
    board_id = 38

    #----------------------- 1) COLLECT DATA FROM LIVE STREAM ----------------------
    if (filename is None):
        # Prepares the board for reading data
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

        # Read data
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
        eeg_data = data[eeg_channels]


    #----------------------- 2) COLLECT DATA FROM CSV FILE ----------------------
    else:
        eeg_channels = BoardShim.get_eeg_channels(board_id)
        eeg_data = DataFilter.read_file(filename) #reads file back

    #----------------------- RETURN DATASET ----------------------
    return eeg_channels, eeg_data

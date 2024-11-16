from preprocessData import*
from processData import*
from loggingData import*

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time

def main():
    # Setup
    params = BrainFlowInputParams()
    params.serial_port = 'COM6'
    board_id = 38
    warningLog = []

    #----------------------- TEST CONNECTION FOR READING DATA ----------------------
    try:
        board_id = 38
        board = BoardShim(board_id, params)
        board.prepare_session()
        print("Successfully prepared physical board.")

        # #Releases the board session
        # board.release_session()

    except Exception as e:
        print(e)
        #If the device cannot be found or is being used elsewhere, creates a synthetic board instead
        print("Device could not be found or is being used by another program, creating synthetic board.")
        board_id = BoardIds.SYNTHETIC_BOARD
        board = BoardShim(board_id, params)
        board.prepare_session()

        # #Releases the board session
        # board.release_session()
    
    #----------------------- START STREAM ----------------------
    try:
        # Start the EEG data stream
        board.start_stream()
        print("Streaming data...")
        
        # Infinite loop to collect data every 5 seconds
        while True:
            time.sleep(5)  # Wait for 5 seconds
            data = board.get_current_board_data(150)
            
            #We want to isolate just the eeg data
            eeg_channels = board.get_eeg_channels(board_id)
            eeg_channels = [c-1 for c in eeg_channels] #readjust channel index [1,2,3,4] to [0,1,2,3]
            eeg_data = data[eeg_channels]

            #Preprocess data - filter noise and anomaly
            eeg_channels, eeg_data = preprocessData(eeg_channels, eeg_data)

            #Analyze data
            thetaBetaRatio, alphaThetaRation = processData(eeg_channels, eeg_data)
            print("Theta/Beta ratio is: %f" %thetaBetaRatio)
            print("Alpha/Theta ratio is: %f" %alphaThetaRation)
            
            #Logging data
            warningLog, warning = loggingData(warningLog, thetaBetaRatio, alphaThetaRation)
            print(warningLog)
            if (warning == 1):
                print("Fatigue detected, please take a rest!")
            elif (warning == 2):
                print("Severe fatigue detected, please rest!")
            
            print("")
            

    except KeyboardInterrupt:
        print("Stopping the stream...")
    finally:
        # Release resources
        board.stop_stream()
        board.release_session()

if __name__ == "__main__":
   main()
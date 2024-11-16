from loadRawData import*
from preprocessData import*
from processData import*

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter
import time

def main():
    # Setup
    params = BrainFlowInputParams()
    params.serial_port = 'COM6'
    board_id = 38

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
            time.sleep(10)  # Wait for 5 seconds
            data = board.get_current_board_data(150)
            #print(data.shape)
            
            #We want to isolate just the eeg data
            eeg_channels = board.get_eeg_channels(board_id)
            eeg_channels = [c-1 for c in eeg_channels] #readjust channel index
            eeg_data = data[eeg_channels]

            #Preprocess data
            eeg_channels, eeg_data = preprocessData(eeg_channels, eeg_data)

            dominateWave, thetaBetaRatio = processData(eeg_channels, eeg_data)
            print("The dominant wave is: " + dominateWave)
            print("Theta/Beta ratio is: %f" %thetaBetaRatio)
            if (dominateWave == "Alpha" and thetaBetaRatio > 1):
                print("Fatigue detected")
            elif (dominateWave == "Theta"):
                print("Fatigue detected")
            elif (dominateWave == "Delta"):
                print("Likely not conscious")
            

    except KeyboardInterrupt:
        print("Stopping the stream...")
    finally:
        # Release resources
        board.stop_stream()
        board.release_session()

if __name__ == "__main__":
   main()
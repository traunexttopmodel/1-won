from flask import Flask, jsonify
from preprocessData import *
from processData import *
from loggingData import loggingData

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time
import threading

app = Flask(__name__)



warning_log = []

# Function to read and process brain wave data in real time
def brain_wave_monitor():
    global current_warning, warning_log

    # Setup BrainFlow board parameters
    params = BrainFlowInputParams()
    params.serial_port = 'COM6'  # Adjust according to your device setup
    board_id = 38

    # Attempt to establish a connection to the board
    try:
        board = BoardShim(board_id, params)
        board.prepare_session()
    except Exception as e:
        print(e)
        print("Device could not be found or is being used by another program. Creating a synthetic board.")
        board_id = BoardIds.SYNTHETIC_BOARD.value
        board = BoardShim(board_id, params)
        board.prepare_session()

    # Start the EEG data stream
    try:
        board.start_stream()
        print("Streaming data...")

        while True:
            time.sleep(5)
            data = board.get_current_board_data(150)
            eeg_channels = [c - 1 for c in board.get_eeg_channels(board_id)]
            eeg_data = data[eeg_channels]

            eeg_channels, eeg_data = preprocessData(eeg_channels, eeg_data)
            thetaBetaRatio, alphaThetaRation = processData(eeg_channels, eeg_data)

            warning_log, current_warning = loggingData(warning_log, thetaBetaRatio, alphaThetaRation)
            print(f"Current warning: {current_warning}")
            print(f"Warning log: {warning_log}")

    except KeyboardInterrupt:
        print("Stopping the stream...")
    finally:
        board.stop_stream()
        board.release_session()


# Flask route to get the current warning state
@app.route('/brainwaves', methods=['GET'])
def get_brainwave_state():
    return jsonify({'warning': current_warning, 'log': warning_log})

# Main function to run Flask and the brain wave monitor
if __name__ == '__main__':
    # Start the brain wave monitoring in a separate thread
    monitor_thread = threading.Thread(target=brain_wave_monitor)
    monitor_thread.daemon = True  # Daemon thread will close when the main program exits
    monitor_thread.start()

    # Run the Flask server
    app.run(debug=True, use_reloader=False)

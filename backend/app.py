from flask import Flask, jsonify
from preprocessData import *
from processData import *
from loggingData import loggingData

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time
import threading

app = Flask(__name__)

# Global variables to store the current warning state and log
current_warning = 0
warning_log = []

# Function to read and process brain wave data in real time
def brain_wave_monitor():
    global current_warning, warning_log

    # Setup
    params = BrainFlowInputParams()
    params.serial_port = 'COM6'
    board_id = 38

    # Test connection for reading data
    try:
        board = BoardShim(board_id, params)
        board.prepare_session()
    except Exception as e:
        print(e)
        print("Device could not be found or is being used by another program, creating synthetic board.")
        board_id = BoardIds.SYNTHETIC_BOARD
        board = BoardShim(board_id, params)
        board.prepare_session()

    # Start the EEG data stream
    try:
        board.start_stream()
        print("Streaming data...")

        # Infinite loop to collect data every 5 seconds
        while True:
            time.sleep(5)  # Wait for 5 seconds
            data = board.get_current_board_data(150)

            # Isolate EEG data
            eeg_channels = board.get_eeg_channels(board_id)
            eeg_channels = [c - 1 for c in eeg_channels]  # Adjust channel index
            eeg_data = data[eeg_channels]

            # Preprocess data - filter noise and anomaly
            eeg_channels, eeg_data = preprocessData(eeg_channels, eeg_data)

            # Analyze data
            theta_beta_ratio, alpha_theta_ratio = processData(eeg_channels, eeg_data)

            # Logging data using the loggingData function
            warning_log, warning = loggingData(warning_log, theta_beta_ratio, alpha_theta_ratio)
            current_warning = warning  # Update the global warning state

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
    app.run(debug=True)

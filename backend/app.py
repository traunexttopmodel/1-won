from flask import Flask, request, jsonify
from preprocessData import preprocessData
from loggingData import loggingData
from processData import processData
from flask_cors import CORS
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time
import threading

app = Flask(__name__)
CORS(app)

# Global variables to store the current warning state and log
current_warning = 0
warning_log = []

# Function to read and process brain wave data in real-time
def brain_wave_monitor():
    global current_warning, warning_log

    # Setup BrainFlow board parameters
    params = BrainFlowInputParams()
    params.serial_port = 'COM6'  # Replace with your actual serial port if needed
    board_id = 38  # Adjust according to your device

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

        # Infinite loop to collect data every 5 seconds
        while True:
            time.sleep(5)  # Collect data every 5 seconds
            data = board.get_current_board_data(150)

            # Extract EEG channels
            eeg_channels = board.get_eeg_channels(board_id)
            eeg_channels = [c - 1 for c in eeg_channels]  # Adjust channel indices
            eeg_data = data[eeg_channels]

            # Preprocess and analyze data
            eeg_channels, eeg_data = preprocessData(eeg_channels, eeg_data)
            theta_beta_ratio, alpha_theta_ratio = processData(eeg_channels, eeg_data)

            # Log warnings and update the global warning state
            warning_log, warning = loggingData(warning_log, theta_beta_ratio, alpha_theta_ratio)
            current_warning = warning  # Update the current warning state

            # Print warnings to the console
            print(f"Received data. Theta/Beta ratio: {theta_beta_ratio:.2f}, Alpha/Theta ratio: {alpha_theta_ratio:.2f}")
            if warning == 1:
                print("Mild warning: Fatigue detected.")
            elif warning == 2:
                print("Severe warning: Significant drowsiness detected.")
            else:
                print("No warning: Normal state.")

    except KeyboardInterrupt:
        print("Stopping the stream...")
    finally:
        board.stop_stream()
        board.release_session()

# Flask route to get the current warning state
@app.route('/brainwaves', methods=['GET'])
def get_brainwave_state():
    return jsonify({'warning': current_warning, 'log': warning_log})

# Flask route for processing EEG data (if needed for POST requests)
@app.route('/process-eeg', methods=['POST'])
def process_eeg_data():
    data = request.json
    eeg_data = data.get('eeg_data')
    eeg_channels = data.get('eeg_channels')

    if not eeg_data or not eeg_channels:
        return jsonify({'error': 'Invalid data'}), 400

    # Preprocess and process the data
    eeg_channels, eeg_data = preprocessData(eeg_channels, eeg_data)
    theta_beta_ratio, alpha_theta_ratio = processData(eeg_channels, eeg_data)

    global warning_log
    warning_log, warning = loggingData(warning_log, theta_beta_ratio, alpha_theta_ratio)

    response = {
        "theta_beta_ratio": theta_beta_ratio,
        "alpha_theta_ratio": alpha_theta_ratio,
        "warning": warning,
        "warning_log": warning_log
    }

    return jsonify(response)

# Main function to start the Flask app and brain wave monitor
if __name__ == '__main__':
    # Start brain wave monitoring in a separate thread
    monitor_thread = threading.Thread(target=brain_wave_monitor)
    monitor_thread.daemon = True  # Daemon thread will close when the main program exits
    monitor_thread.start()

    # Run the Flask server
    app.run(debug=True)


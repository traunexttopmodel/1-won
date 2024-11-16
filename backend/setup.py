#--------------------------------------------------------------------------------
# SUMMARY: This function test connection to Muse 2 first,
#          so loadRawData can be called without resetting and testing every time later on.
#          It returns 38 (Muse 2 boardId) if can connect, -1 (synthetic) if can't
#--------------------------------------------------------------------------------

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter
import time
import os

def setup():
    # Setup
    params = BrainFlowInputParams()
    params.serial_port = 'COM6'
    board_id = 38

    # Prepares the board for reading data
    try:
        board_id = 38
        board = BoardShim(board_id, params)
        board.prepare_session()
        print("Successfully prepared physical board.")

        #Releases the board session
        board.release_session()
        return 38

    except Exception as e:
        print(e)
        #If the device cannot be found or is being used elsewhere, creates a synthetic board instead
        print("Device could not be found or is being used by another program, creating synthetic board.")
        board_id = BoardIds.SYNTHETIC_BOARD
        board = BoardShim(board_id, params)
        board.prepare_session()

        #Releases the board session
        board.release_session()
        return -1
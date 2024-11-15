from loadRawData import*
from preprocessData import*
from processData import*

def main():

    #hardcoding for simplicty right now, could code again to dynamic later
    #--------------------------------------------------------------------------------
    # LOADING RAW EEG DATA
    #--------------------------------------------------------------------------------
    loadRawDataOption = 1 #0 if live stream, 1 if load from CSV file
    filename = 'eeg_data_test_1.csv' 

    if (loadRawDataOption == 0): #live stream
        eeg_channels, eeg_data = loadRawData()
    else: #csv fle
        eeg_channels, eeg_data = loadRawData(filename)

    #--------------------------------------------------------------------------------
    # SAVE RAW EEG DATASET IF WANT TO
    #--------------------------------------------------------------------------------
    saveEegData = 0 #0 if not, 1 if yes

    if (saveEegData == 1):
        DataFilter.write_file(eeg_data, 'eeg_data_test.csv', 'w') #Writes into a csv file in the current directory
    
    #--------------------------------------------------------------------------------
    # PREPROCESS DATA - FILTERING
    #--------------------------------------------------------------------------------
    eeg_channels, eeg_data = preprocessData(eeg_channels, eeg_data)

    #--------------------------------------------------------------------------------
    # PROCESS DATA - PLOT PSD & FIND BANDPOWER
    #--------------------------------------------------------------------------------
    processData(eeg_channels, eeg_data)

if __name__ == "__main__":
   main()
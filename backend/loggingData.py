#--------------------------------------------------------------------------------
# SUMMARY: This function logs the last 10 brainwave evaluations.
#          If it pass a threshold ratio (eg. 50% theta or delta waves in the last 20 logs) -> send warning
#--------------------------------------------------------------------------------

import statistics

def loggingData(warningLog, newBrainwave, thetaBetaRatio, thetaAlphaRatio):

    warning = 0

    # Label new data as fatigue or not
    if (thetaBetaRatio > 1.5 and thetaAlphaRatio > 1.5):
        if (thetaBetaRatio > 2 and thetaAlphaRatio > 2):
            warning = 2 #big chime
        else:
            warning = 1 #small chime

    # Log it
    if(len(warningLog) < 10):
        warningLog.append(warning)
        return warningLog, 0
    
    else:
        warningLog = warningLog[1:] # Remove first element (oldest data)
        warningLog.append(warning)

        return warningLog, statistics.median(warningLog)

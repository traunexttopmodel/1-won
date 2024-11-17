#--------------------------------------------------------------------------------
# SUMMARY: This function logs the lastest 10 brainwave evaluations.
#
#          The reason we log the fatigue evaluation of 5-second periods
#          is because the Theta/Beta and Alpha/Theta ratio significantly fluctuates 
#          between each time period.
#
#          Hence, to evaluate the overall the fatigue level over a period of time (in our case, 10*5s = 50s),
#          we decided to take the median value of the last 10 warning evaluations.
#          As our data is evaluated in real time, taking the average instead of the median will
#          result in accounting for extreme values happening 6,7 logs ago - outdated data
#--------------------------------------------------------------------------------

import statistics

def loggingData(warningLog, thetaBetaRatio, alphaThetaRation):

    warning = 0

    # Label warning
    if (thetaBetaRatio > 1.5 and alphaThetaRation < 1.5):
        if (thetaBetaRatio > 2 and alphaThetaRation < 1):
            warning = 2 #big chime
        else:
            warning = 1 #small chime

    # Log it
    if(len(warningLog) < 10):
        warningLog.append(warning)
        return warningLog, 0 #not enough data to evaluate general fatigue level yet
    
    else:
        warningLog = warningLog[1:] # Remove first element (oldest data)
        warningLog.append(warning)

        return warningLog, statistics.median(warningLog)
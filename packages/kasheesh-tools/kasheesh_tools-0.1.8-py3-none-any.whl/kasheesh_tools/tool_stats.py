
from statsmodels.tsa.stattools import adfuller
import pandas as pd
from kasheesh_tools.tool_logger import get_my_logger

def adf_summary(df, autolag='AIC', pvalue_threshold=0.05):
    logger = get_my_logger(name="adf_summary", level="INFO")
    logger.info('Results of Augmented Dickey-Fuller Test:')
    dftest = adfuller(df, autolag=autolag)
    dfoutput = pd.Series(dftest[0:4], index=['T-Test Statistic','p-value','#Lags Used','Number of Observations Used'])

    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value

    print(dfoutput)
    if dftest[1] > pvalue_threshold:
        logger.info("Failed to reject H0(the data is non-stationary). This data is non-stationary, cannot use time series prediction")
    else:
        logger.info("Rejecting H0(the data is non-stationary). This data is stationary, can use time series prediction")

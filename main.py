import yfinance as yf
import pandas as pd
from pandas.tseries.offsets import DateOffset
import numpy as np

# Getting VIX data in a data frame
vix_df = yf.download("^VIX")

# Building the MA condition ( 30 days moving average)
vix_df['MA'] = vix_df.Close.rolling('30D').mean()

# Filtering the data. Buys if the VIX ( Cboe Volatility Index) rises by more 
# than 50% of it's 1-month moving average
vix_df_filt = vix_df[vix_df.Close > 1.5 * vix_df.MA]

series = pd.Series(vix_df_filt.index).diff()/np.timedelta64(1,'D') >= 30

series[0] = True

signals = vix_df_filt[series.values]

# Getting the S&P500 data 
sp_df = yf.download("^GSPC",start ='1990-01-01')

returns = []

# The strategy buys the S&P500 and hold it for six months after the buy signal 
for i in range(len(signals)):
    subdf = sp_df[(sp_df.index >= signals.index[i]) & (sp_df.index <= signals.index[i] +DateOffset(months=6) )]
    returns.append((subdf.Close.pct_change() + 1).prod())

# Results after each buy signals
foreachsignal_returns = (pd.Series(returns)-1)*100

# Mean after all the buys signals
meansignal_returns = (pd.Series(returns)-1).mean()*100

print("The result after each signal is: ",foreachsignal_returns)
print("The mean result is: ",meansignal_returns,"%")





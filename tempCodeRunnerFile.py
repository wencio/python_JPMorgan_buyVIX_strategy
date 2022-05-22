import yfinance as yf
import pandas as pd
import numpy as np


vix_df = yf.download("^VIX")

vix_df['MA'] = vix_df.Close.rolling('30D').mean()

vix_df_filt = vix_df[vix_df.Close > 1.5 * vix_df.MA]

print(vix_df_filt.index)




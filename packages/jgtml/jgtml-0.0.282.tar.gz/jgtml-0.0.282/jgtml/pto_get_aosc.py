#%%
import pandas as pd
import numpy as np
from jgtutils.jgtconstants import DATE,ZLCB,ZLCS

fn="../samples/cds2.csv"


df=pd.read_csv(fn)

# %%
df
# %%
df.reset_index(drop=False, inplace=True)

df[DATE]
# %%
c=0
out_sell_name="vaos"
out_buy_name="vaob"
def count_bars_before_zero_line_cross(df):
    bars_before_signal = 0
    for i in range(len(df) - 1, -1, -1):
      prev_row = df.iloc[i]
      if prev_row[ZLCS] or prev_row[ZLCB]:
        break
      bars_before_signal += 1
    return bars_before_signal

bars_before_signal = count_bars_before_zero_line_cross(df)
print("Bars before signal:",bars_before_signal)
# for index, row in df.iterrows():
#   zeroLineCrossBuy = row[ZLCS]
#   zeroLineCrossSell = row[ZLCB]
  
# %%

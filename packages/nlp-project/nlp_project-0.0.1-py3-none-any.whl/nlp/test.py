# for file system import
from imit_main import imit_signal as imit # for file import
from nlp_main import nlp_signal as nlp # for file import

# for install import
#from nlp.imit_main import imit_signal as imit # for file import
#from nlp.nlp_main import nlp_signal as nlp # for file import

import numpy as np
import pandas as pd

def getSignal(*args):
    try:
        return imit(*args)
    except Exception as e:
        print(e)


df = pd.read_csv('src/nlp/test.csv')
df.drop(['Unnamed: 0'], inplace=True, axis=1)

df['regresult'] = df.apply(lambda row: getSignal(  row['open'], row['high'], row['a'], row['b'], row['vc'], row['ema-26'], row['ema-12'], row['macd'],
                                                row['macdsignal'], row['macd-histogram'], row['low'], row['grad-histogram'],
                                                row['mean-grad-hist'], row['close'], row['pct-change'], row['volume'], row['grad-vol-sma'],
                                                row['ratio4'], row['rsi-05'], row['rsi-15'], row['sma-25'], row['short-close-gradient'],
                                                row['long-close-gradient'], row['close-gradient-neg'], row['grad-sma-25'], row['long_kdj'],
                                                row['long_grad_kdj'], row['long_jcrosk'], row['short_kdj'], row['short_grad_kdj']
                                              ), axis=1)


# Convert Series to list
string_series = pd.Series(df['regresult'].tolist())

# Function to create sliding windows
def sliding_windows(series=string_series, window_size=5):
    for i in range(len(series) - window_size + 1):
        yield series[i:i + window_size]

predictions = [np.nan] * len(string_series)  # Start with NaN, predictions will overwrite later

# Create sliding windows and predict
window_size = 5  # Sliding window size of 5
for i, window in enumerate(sliding_windows(series=string_series, window_size=5)):
    pred = nlp(window)  # Replace with your actual model's predict function
    predictions[i + window_size - 1] = pred

df['nlpreds'] = predictions

print(len(df[df['actions'] == df['nlpreds']]), len(df))
print(df.tail())
import numpy as np
import pandas as pd
from sklearn import svm

data = pd.read_csv('沪深300.csv')
data['DateTime'] = pd.to_datetime(data['DateTime'])
data = data.resample('W', on="DateTime").last()
data.dropna(inplace = True)
data.set_index('DateTime', inplace=True)
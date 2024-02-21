import numpy as np
import pandas as pd
import seaborn as sns
import glob
import os

# Extract geographic location and other info from the filename
file = '/Users/cfranken/GE_output_test/Amazon_Test_2018-01-01_2022-01-01_-55.0_1.0_200.0.csv'
file2 = '/Users/cfranken/GE_output_test/Amazon_Test_2018-01-01_2022-01-01_-55.0_1.0_2000.0.csv'
filename = os.path.basename(file)
parts = filename.split('_')
lat, lon, res = float(parts[-2]), float(parts[-3]), float(parts[-1].replace('.csv', ''))
 #print(file)
# Read cloud fraction data
#try:
data = pd.read_csv(file)
df1 = data.rename(columns={'cloud_free_fraction02': 'cf_200'})
data2 = pd.read_csv(file2)
df2 = data2.rename(columns={'cloud_free_fraction02': 'cf_2000'})
time_ = data['system:index']
time_2 = data2['system:index']
df1['timestamp'] = [pd.to_datetime(s.split('_')[0],format='%Y%m%dT%H%M%S') for s in time_]
df2['timestamp'] = [pd.to_datetime(s.split('_')[0],format='%Y%m%dT%H%M%S') for s in time_2]
result = pd.merge(df1[['timestamp', 'cf_200']], df2[['timestamp', 'cf_2000']], on='timestamp', how='inner')
result['Date'] = result['timestamp'].dt.strftime('%Y-%m-%d')
result[['Date','cf_200', 'cf_2000']].to_csv('data/subset_data.csv', index=False)
parquet_file = 'your_file.parquet'
data.to_parquet(parquet_file, engine='pyarrow')
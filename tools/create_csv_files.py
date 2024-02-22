import numpy as np
import pandas as pd
import seaborn as sns
import pyarrow as pa
import pyarrow.feather as feather
import glob
import os

def process_files(lon, lat):
    try:
        # Extract geographic location and other info from the filename
        file = f'/Users/cfranken/GE_output_test/Amazon_Test_2018-01-01_2022-01-01_{lon}.0_{lat}.0_200.0.csv'
        file2 = f'/Users/cfranken/GE_output_test/Amazon_Test_2018-01-01_2022-01-01_{lon}.0_{lat}.0_2000.0.csv'
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
        result = pd.merge(df1[['timestamp', 'cf_200']], df2[['timestamp', 'cf_2000','domain_pixel_count']], on='timestamp', how='inner')
        result['Date'] = result['timestamp'].dt.strftime('%Y-%m-%d')
        filtered_df = result[result['domain_pixel_count'] > 5000000]
        outfile = f'data/sentinel2_clouds_{lon}_{lat}.csv'
        filtered_df[['Date','cf_200', 'cf_2000']].to_csv(outfile, index=False)
    except:
        print("Error")


# Define start and end points for latitude and longitude
start_lat, end_lat = -10, 2  # for example, from 10 to 20 degrees latitude
start_lon, end_lon = -80, -30  # for example, from 30 to 40 degrees longitude

# Generate pairs of latitudes and longitudes in 1 degree steps
lat_lon_pairs = [(lat, lon) for lat in range(start_lat, end_lat + 1) 
                           for lon in range(start_lon, end_lon + 1)]

# Display the generated pairs
for pair in lat_lon_pairs:
    print(pair)
    process_files(pair[1],pair[0])

parquet_file = 'your_file.parquet'
data.to_parquet(parquet_file, engine='pyarrow')

# Convert the pandas DataFrame to an Arrow Table
table = pa.Table.from_pandas(result[['Date','cf_200', 'cf_2000']])

# Save the Arrow Table to an IPC file (Feather format)
feather.write_feather(table, 'data/subset_data.feather', compression=None)
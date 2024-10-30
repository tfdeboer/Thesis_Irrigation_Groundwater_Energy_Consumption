import os
import pandas as pd

# Function to calculate the missing data percentage
def calculate_missing_percentage(start_date, end_date, total_years=58):
    if start_date is None or end_date is None:
        return 100.0
    total_period_years = (end_date - start_date).days / 365.25
    return 100 - (total_period_years / total_years * 100)

# Function to process individual well data files
def process_well_data(file_path):
    try:
        df = pd.read_csv(file_path, sep='\s+', skiprows=13)
        if 'datetime' not in df.columns:
            raise ValueError(f"Column 'datetime' not found in {file_path}")
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        start_date = df['datetime'].min()
        end_date = df['datetime'].max()
        return start_date, end_date, df
    except Exception as e:
        print(f"Error reading time series for well {file_path}: {e}")
        return None, None, None

# Base directory and output path
base_directory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_GLD_well'
output_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/wells_data_GLD_1958_2015_locations.csv'

# Columns for the output dataframe
columns = ['well_id', 'time_range_start', 'time_range_end', 'x', 'y', 'screen_bottom', 'ground_level', 'screen_top', 'tube_top', 'missing_data_percentage']

# List to hold the data
data = []

# Loop through each well directory
well_count = 0
error_count = 0

for well_id in os.listdir(base_directory):
    well_path = os.path.join(base_directory, well_id)
    if os.path.isdir(well_path):
        well_count += 1
        txt_file = os.path.join(well_path, f'gw_bro_{well_id}.txt')
        if os.path.isfile(txt_file):
            with open(txt_file, 'r') as f:
                metadata = {}
                for _ in range(13):
                    line = f.readline().strip().split(':')
                    if len(line) == 2:
                        metadata[line[0].strip()] = line[1].strip()
                start_date, end_date, df = process_well_data(txt_file)
                if start_date and end_date:
                    missing_data_percentage = calculate_missing_percentage(start_date, end_date)
                    data.append([
                        well_id,
                        start_date.strftime('%Y-%m-%d') if start_date else '',
                        end_date.strftime('%Y-%m-%d') if end_date else '',
                        metadata.get('x', ''),
                        metadata.get('y', ''),
                        metadata.get('screen_bottom', ''),
                        metadata.get('ground_level', ''),
                        metadata.get('screen_top', ''),
                        metadata.get('tube_top', ''),
                        missing_data_percentage
                    ])
                else:
                    error_count += 1

# Create the dataframe and save to CSV
df = pd.DataFrame(data, columns=columns)
df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")
print(f"Number of wells processed: {well_count}")
print(f"Number of wells with errors: {error_count}")

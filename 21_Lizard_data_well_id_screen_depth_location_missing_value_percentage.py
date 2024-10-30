import pickle
import pandas as pd
import os

# Inlezen van het opgeslagen pklz-bestand
outputDirectory = '../../input/timeseries_gw_Netherlands_hydropandas/'
pklz_file = outputDirectory + 'gw_bro_Netherlands.pklz'

with open(pklz_file, 'rb') as f:
    gw_bro = pickle.load(f)

# Parameters voor de periode
start_date = pd.Timestamp('1958-01-01')
end_date = pd.Timestamp('2015-12-31')
total_period = (end_date - start_date).days

# Functie om percentage ontbrekende data te berekenen
def calculate_missing_percentage(time_range_start, time_range_end):
    if pd.isna(time_range_start) or pd.isna(time_range_end):
        return 100.0
    period_present = (time_range_end - time_range_start).days
    missing_days = total_period - period_present
    missing_percentage = (missing_days / total_period) * 100
    return max(0, min(100, missing_percentage))

# Berekeningen
all_wells = []

# Itereren door de rijen om de gegevens te extraheren
for index, row in gw_bro.iterrows():
    well_number = row['monitoring_well']
    tube_nr = row['tube_nr']
    well_id = f"{well_number}_{tube_nr}"
    x = row['x']
    y = row['y']
    screen_bottom = row.get('screen_bottom', None)
    ground_level = row.get('ground_level', None)
    screen_top = row.get('screen_top', None)
    tube_top = row.get('tube_top', None)
    time_series_data = row['obs']
    
    if not time_series_data.empty:
        time_series_df = pd.DataFrame(time_series_data)
        time_series_df.reset_index(inplace=True)
        time_series_df.columns = ['datetime', 'value', 'flag', 'comment']
        
        # Bepaal de tijdsrange
        time_range_start = time_series_df['datetime'].min()
        time_range_end = time_series_df['datetime'].max()
        
        # Filter de data tussen 1958 en 2015
        filtered_data = time_series_df[(time_series_df['datetime'] >= start_date) & (time_series_df['datetime'] <= end_date)]
        
        missing_percentage = calculate_missing_percentage(time_range_start, time_range_end)
        
        all_wells.append([well_id, time_range_start, time_range_end, x, y, screen_bottom, ground_level, screen_top, tube_top, missing_percentage])
    else:
        all_wells.append([well_id, None, None, x, y, screen_bottom, ground_level, screen_top, tube_top, 100.0])

# Data opslaan in een DataFrame en dan naar een CSV-bestand
columns = ['well_id', 'time_range_start', 'time_range_end', 'x', 'y', 'screen_bottom', 'ground_level', 'screen_top', 'tube_top', 'missing_percentage']
all_wells_df = pd.DataFrame(all_wells, columns=columns)

# Resultaten opslaan in een CSV-bestand
output_file = os.path.join(outputDirectory, 'wells_data_1958_2015_locations.csv')
all_wells_df.to_csv(output_file, index=False)

print(f"Data opgeslagen in {output_file}")

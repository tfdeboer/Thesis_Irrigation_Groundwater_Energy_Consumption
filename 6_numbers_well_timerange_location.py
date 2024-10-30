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

# Berekeningen
total_wells = len(gw_bro['monitoring_well'].unique())
wells_with_full_data = []
wells_with_partial_data = []
wells_with_no_data = []
all_wells = []

# Itereren door de rijen om de gegevens te extraheren
for index, row in gw_bro.iterrows():
    well_number = row['monitoring_well']
    tube_nr = row['tube_nr']
    well_id = f"{well_number}_{tube_nr}"
    x = row['x']
    y = row['y']
    time_series_data = row['obs']
    
    if not time_series_data.empty:
        time_series_df = pd.DataFrame(time_series_data)
        time_series_df.reset_index(inplace=True)
        time_series_df.columns = ['datetime', 'value', 'flag', 'comment']
        
        # Bepaal de tijdsrange
        time_range_start = time_series_df['datetime'].min()
        time_range_end = time_series_df['datetime'].max()
        
        all_wells.append([well_id, time_range_start, time_range_end, x, y])
        
        # Filter de data tussen 1958 en 2015
        filtered_data = time_series_df[(time_series_df['datetime'] >= start_date) & (time_series_df['datetime'] <= end_date)]
        
        if not filtered_data.empty:
            if filtered_data['datetime'].min() <= start_date and filtered_data['datetime'].max() >= end_date:
                wells_with_full_data.append([well_id, time_range_start, time_range_end, x, y])
            else:
                wells_with_partial_data.append([well_id, time_range_start, time_range_end, x, y])
        else:
            wells_with_no_data.append([well_id, time_range_start, time_range_end, x, y])
    else:
        wells_with_no_data.append([well_id, None, None, x, y])
        all_wells.append([well_id, None, None, x, y])

# Resultaten afdrukken
print(f"Aantal wells: {total_wells}")
print(f"Aantal wells met volledige data tussen 1958 t/m 2015: {len(wells_with_full_data)}")
print(f"Aantal wells met gedeeltelijke data tussen 1958 t/m 2015: {len(wells_with_partial_data)}")
print(f"Aantal wells zonder data tussen 1958 t/m 2015: {len(wells_with_no_data)}")

# Opslaan in een CSV-bestand
output_file = os.path.join(outputDirectory, 'wells_data_1958_2015_location.csv')
with open(output_file, 'w') as f:
    f.write("Wells with full data range between 1958 and 2015\n")
    f.write("well_id,time_range_start,time_range_end,x,y\n")
    for well in wells_with_full_data:
        f.write(f"{well[0]},{well[1]},{well[2]},{well[3]},{well[4]}\n")
    
    f.write("\nWells with partial data range between 1958 and 2015\n")
    f.write("well_id,time_range_start,time_range_end,x,y\n")
    for well in wells_with_partial_data:
        f.write(f"{well[0]},{well[1]},{well[2]},{well[3]},{well[4]}\n")
    
    f.write("\nWells with no data between 1958 and 2015\n")
    f.write("well_id,time_range_start,time_range_end,x,y\n")
    for well in wells_with_no_data:
        f.write(f"{well[0]},{well[1]},{well[2]},{well[3]},{well[4]}\n")
    
    f.write("\nAll wells\n")
    f.write("well_id,time_range_start,time_range_end,x,y\n")
    for well in all_wells:
        f.write(f"{well[0]},{well[1]},{well[2]},{well[3]},{well[4]}\n")

print(f"Data opgeslagen in {output_file}")

import os
import pickle
import pandas as pd

# Inlezen van het opgeslagen pklz-bestand
outputDirectory = '../../input/timeseries_gw_Netherlands_hydropandas/'
pklz_file = outputDirectory + 'gw_bro_Netherlands.pklz'

with open(pklz_file, 'rb') as f:
    gw_bro = pickle.load(f)

# Mappen aanmaken voor de outputbestanden
locations_output_dir = os.path.join(outputDirectory, 'location_and_tubenumbers')
well_numbers_output_dir = os.path.join(outputDirectory, 'well_numbers_data')

if not os.path.exists(locations_output_dir):
    os.makedirs(locations_output_dir)

if not os.path.exists(well_numbers_output_dir):
    os.makedirs(well_numbers_output_dir)

# Dataframe voor x, y en well_number
location_data = []

# Itereren door de rijen om de gegevens te extraheren
for index, row in gw_bro.iterrows():
    well_number = row['monitoring_well']
    x = row['x']
    y = row['y']
    tube_nr = row['tube_nr']
    tube_suffix = '' if tube_nr == 1 else f'_{tube_nr}'
    well_id = f"{well_number}{tube_suffix}"
    location_data.append([x, y, well_id])

    # Tijdreeks en metadata opslaan per well_number
    time_series_data = row['obs']
    if not time_series_data.empty:
        time_series_df = pd.DataFrame(time_series_data)
        time_series_df.reset_index(inplace=True)
        time_series_df.columns = ['datetime', 'value', 'flag', 'comment']  # Pas de kolommen aan naar behoefte

        # Opslaan van de tijdreeks data
        well_output_file = os.path.join(well_numbers_output_dir, f'{well_id}.csv')
        time_series_df.to_csv(well_output_file, index=False)

# Opslaan van de x, y en well_number data
location_df = pd.DataFrame(location_data, columns=['x', 'y', 'well_number'])
location_output_file = os.path.join(locations_output_dir, 'location_and_tubenumbers.csv')
location_df.to_csv(location_output_file, index=False)

print("Data opschoning en export voltooid.")

import os
import hydropandas as hpd
import pickle
import pprint

# Pad naar het bestand met well IDs
well_ids_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/well_ids.txt'

# Output directory
output_base_directory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_GLD_well/'

# Maak de output base directory aan als deze nog niet bestaat
if not os.path.exists(output_base_directory):
    os.makedirs(output_base_directory)

# Lees de well IDs uit het bestand
with open(well_ids_path, 'r') as f:
    well_ids = f.read().splitlines()

# Zoek het startpunt in de lijst van well IDs
start_well_id = 'GLD000000000001'
try:
    start_index = well_ids.index(start_well_id)
    well_ids = well_ids[start_index:]
except ValueError:
    print(f"Start well ID {start_well_id} not found in the list.")
    well_ids = []

# Loop door elke well ID en haal de data op
for well_id in well_ids:
    try:
        # Maak een directory voor de huidige well ID
        output_directory = os.path.join(output_base_directory, well_id)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Haal de data op voor de huidige well ID
        gw_bro = hpd.GroundwaterObs.from_bro(well_id, 1)

        # Sla de data op als pickle bestand
        pickle_file_path = os.path.join(output_directory, f'gw_bro_{well_id}.pklz')
        gw_bro.to_pickle(pickle_file_path)

        # Sla de data op als text bestand
        with open(os.path.join(output_directory, f'gw_bro_{well_id}.txt'), 'a') as f:
            pprint.pprint(gw_bro, stream=f)

        # Sla de data op als Excel bestand
        excel_file_path = os.path.join(output_directory, f'gw_bro_{well_id}.xlsx')
        gw_bro.to_excel(excel_file_path)

        print(f"Data for well ID {well_id} saved successfully.")

    except Exception as e:
        print(f"Failed to process well ID {well_id}: {e}")

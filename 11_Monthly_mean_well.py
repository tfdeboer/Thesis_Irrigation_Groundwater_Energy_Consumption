import os
import pandas as pd

# Pad naar de map met de well data bestanden
input_directory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/well_numbers_data'

# Pad naar de map waar de maandelijkse gemiddelden worden opgeslagen
output_directory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/well_numbers_monthly_mean'

# Maak de output directory aan als deze nog niet bestaat
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop door alle bestanden in de input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        # Lees het CSV bestand
        file_path = os.path.join(input_directory, filename)
        df = pd.read_csv(file_path)

        # Converteer de 'datetime' kolom naar een datetime object
        df['datetime'] = pd.to_datetime(df['datetime'])

        # Verwijder de 'flag' en 'comment' kolommen
        df = df.drop(columns=['flag', 'comment'])

        # Groepeer de gegevens per maand en bereken het gemiddelde
        df_monthly_mean = df.resample('ME', on='datetime').mean().reset_index()

        # Bewaar alleen de 'datetime' en 'value' kolommen
        df_monthly_mean = df_monthly_mean[['datetime', 'value']]

        # Schrijf het resultaat naar een nieuw CSV bestand in de output directory
        output_file_path = os.path.join(output_directory, filename)
        df_monthly_mean.to_csv(output_file_path, index=False)

print("Maandelijkse gemiddelden zijn berekend en opgeslagen in de map:", output_directory)

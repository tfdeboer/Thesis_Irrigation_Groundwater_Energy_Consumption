import os
import pandas as pd

# Pad naar de map met de maandelijkse gemiddelde bestanden
input_directory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/well_numbers_monthly_mean'

# Pad naar de map waar de gemiddelde waarden per well worden opgeslagen
output_directory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/mean_value_per_well'

# Maak de output directory aan als deze nog niet bestaat
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Lijst om de gemiddelde waarden per well op te slaan
mean_values = []

# Loop door alle bestanden in de input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        # Lees het CSV bestand
        file_path = os.path.join(input_directory, filename)
        df = pd.read_csv(file_path)

        # Bereken de gemiddelde waarde, negeer NaN waarden
        mean_value = df['value'].mean()

        # Voeg het well nummer en de gemiddelde waarde toe aan de lijst
        well_number = filename.split('.')[0]
        mean_values.append({'well_number': well_number, 'mean_value': mean_value})

# Zet de lijst om in een DataFrame
mean_df = pd.DataFrame(mean_values)

# Pad naar het output CSV bestand
output_file_path = os.path.join(output_directory, 'mean_value_per_well.csv')

# Schrijf het resultaat naar een CSV bestand
mean_df.to_csv(output_file_path, index=False)

print("Gemiddelde waarden per well zijn berekend en opgeslagen in het bestand:", output_file_path)

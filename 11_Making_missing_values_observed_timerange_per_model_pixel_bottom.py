import os
import pandas as pd

# Define the directory containing the timeseries files
timeseries_dir = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/tables/Observed_data/pixel_timeseries_bottom_layer'

# Define the time range from 1958-01-01 to 2015-12-01 (monthly steps)
date_range = pd.date_range(start='1980-01-01', end='2015-12-01', freq='MS') #later aangepast toen data veranderde

# Initialize a dictionary to store the missing data percentages
missing_data_percentages = {}

# Process each file in the directory
for filename in os.listdir(timeseries_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(timeseries_dir, filename)
        
        # Load the timeseries data
        df = pd.read_csv(file_path, parse_dates=True, index_col=0)
        
        # Reindex to the full date range to include all months
        df = df.reindex(date_range)
        
        # Calculate the percentage of missing data
        missing_percentage = df['groundwater_level'].isna().sum() / len(df) * 100
        
        # Store the result
        missing_data_percentages[filename] = missing_percentage

# Convert the results to a DataFrame for better readability
missing_data_df = pd.DataFrame(list(missing_data_percentages.items()), columns=['File', 'MissingDataPercentage'])
missing_data_df = missing_data_df.sort_values(by='MissingDataPercentage', ascending=False)

# Save the result to a CSV file
missing_data_df.to_csv('/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/missing_data_percentages_bottom_1980_2015.csv', index=False)

print("Missing data percentages saved to 'missing_data_percentages_bottom_1980_2015.csv'") #later aangepast. Bestand wordt in dezelfde map opgeslagen!

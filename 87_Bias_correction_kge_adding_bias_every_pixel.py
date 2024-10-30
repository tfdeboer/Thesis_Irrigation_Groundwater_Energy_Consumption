import os
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from hydroeval import evaluator, kge

# Define file paths
model_data_dir = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/GLOBGM_Well_data_and_locations/data_globgm_top_monthly'
obs_data_dir = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/pixel_timeseries_top_layer'
mapping_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/GLOBGM_Well_data_and_locations/well_locations_top_mapping.csv'
bias_correction_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/output/kge_results/kge_results_top_layer.csv'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/data/shp/NL/Netherlands.shp'
output_dir = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/output/kge_results/'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the mapping file
mapping_df = pd.read_csv(mapping_file)

# Load the bias correction file
bias_correction_df = pd.read_csv(bias_correction_file)
bias_correction_df.set_index('pixel_id', inplace=True)  # Assume 'pixel_id' is in your file

# Initialize a dictionary to store KGE results
kge_results = []

# Function to load timeseries data from a CSV file
def load_timeseries(file_path):
    data = pd.read_csv(file_path, header=0, parse_dates=[0], index_col=0)
    data.index = data.index.to_period('M')  # Convert to monthly period
    return data

# Process each pixel
for index, row in mapping_df.iterrows():
    pixel_id = row['well_id'].replace('.csv', '').replace('Pixel_top_', '')
    model_path = os.path.join(model_data_dir, f'Pixel_top_{pixel_id}.csv')
    obs_path = os.path.join(obs_data_dir, f'Pixel_top_layer_timeseries_{pixel_id}.csv')
    
    print(f"Processing Pixel ID: {pixel_id}")
    print(f"Model Path: {model_path}")
    print(f"Obs Path: {obs_path}")
    
    if os.path.exists(model_path) and os.path.exists(obs_path):
        model_data = load_timeseries(model_path)
        obs_data = load_timeseries(obs_path)
        
        # Fetch the bias correction value from the CSV file
        if pixel_id in bias_correction_df.index:
            bias_correction_value = bias_correction_df.loc[pixel_id, 'bias']  # Adjust the column name if needed
            
            # Apply the bias correction by subtracting the bias value (additive correction)
            model_data_corrected = model_data - bias_correction_value
            
            print(f"Corrected Model data for Pixel ID {pixel_id}:\n", model_data_corrected.head())
            
            # Align the datasets
            combined_data = pd.merge(model_data_corrected, obs_data, left_index=True, right_index=True, how='inner', suffixes=('_model', '_obs'))
            
            print(f"Combined data for Pixel ID {pixel_id} after merging:\n", combined_data.head())
            
            if not combined_data.empty:
                # Filter out rows where either value is NaN
                combined_data = combined_data.dropna(subset=['groundwater_level_model', 'groundwater_level_obs'])
                
                print(f"Combined data for Pixel ID {pixel_id} after dropping NaNs:\n", combined_data.head())
                
                if not combined_data.empty and len(combined_data) > 1:  # Ensure there are enough data points
                    # Perform KGE analysis
                    kge_values = evaluator(kge, combined_data['groundwater_level_model'].to_numpy(), combined_data['groundwater_level_obs'].to_numpy())
                    
                    print(f"KGE values for Pixel ID {pixel_id}:", kge_values)
                    
                    # Extract values and ensure they are scalars before converting to float
                    kge_results.append({
                        'pixel_id': pixel_id, 
                        'lat': row['lat'], 
                        'lon': row['lon'], 
                        'kge': float(kge_values[0][0]),  # Extract the scalar value
                        'correlation': float(kge_values[1][0]),  # Extract the scalar value
                        'bias': float(kge_values[2][0]),  # Extract the scalar value
                        'variability': float(kge_values[3][0])  # Extract the scalar value
                    })  # Save KGE and its components
                else:
                    print(f"Not enough data after merging and dropping NaNs for pixel_id {pixel_id}")
            else:
                print(f"No overlapping dates for pixel_id {pixel_id}")
    else:
        print(f"Files do not exist for Pixel ID: {pixel_id}")

# Convert results to a DataFrame and check contents
kge_df = pd.DataFrame(kge_results)
print("kge_df contents:")
print(kge_df.head())

# Calculate average values for kge, correlation, bias, and variability
avg_kge = kge_df['kge'].mean()
avg_correlation = kge_df['correlation'].mean()
avg_bias = kge_df['bias'].mean()
avg_variability = kge_df['variability'].mean()

# Create a DataFrame for the averages
avg_df = pd.DataFrame([{
    'pixel_id': 'average',
    'lat': None,
    'lon': None,
    'kge': avg_kge,
    'correlation': avg_correlation,
    'bias': avg_bias,
    'variability': avg_variability
}])

# Append the averages to the main DataFrame using pd.concat
kge_df = pd.concat([kge_df, avg_df], ignore_index=True)

# Save KGE results to a CSV file
output_file = os.path.join(output_dir, 'kge_results_top_layer_additive_bias_correction.csv')
kge_df.to_csv(output_file, index=False)

print(f"KGE analysis results saved to {output_file}")

# Plotting the KGE values over the Netherlands
if 'lon' in kge_df.columns and 'lat' in kge_df.columns:
    # Exclude the row with the average values since it has no geometry information
    kge_df_non_avg = kge_df.dropna(subset=['lat', 'lon'])

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(kge_df_non_avg, geometry=gpd.points_from_xy(kge_df_non_avg.lon, kge_df_non_avg.lat))

    # Load the shapefile
    nl_shapefile = gpd.read_file(shapefile_path)

    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    nl_shapefile.plot(ax=ax, color='lightgrey')

    gdf.plot(column='kge', ax=ax, legend=True, cmap='viridis', markersize=50, legend_kwds={'label': "KGE Value", 'orientation': "horizontal"})

    plt.title('KGE Analysis of Groundwater Levels (Additive Bias Correction)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    print(f"KGE analysis results saved to {output_file}")
else:
    print("Error: 'lon' or 'lat' columns are missing in the DataFrame.")
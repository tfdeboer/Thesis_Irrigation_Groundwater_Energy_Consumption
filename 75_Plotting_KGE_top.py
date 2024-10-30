import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Define file paths
results_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/output/kge_results/kge_top_layer_results_cor_bias_var.csv'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/data/shp/NL/Netherlands.shp'

# Load the results data
results_df = pd.read_csv(results_file)

# Convert 'lat' and 'lon' to floats (in case they are not)
results_df['lat'] = results_df['lat'].astype(float)
results_df['lon'] = results_df['lon'].astype(float)

# Create a GeoDataFrame from the results
gdf = gpd.GeoDataFrame(results_df, geometry=gpd.points_from_xy(results_df.lon, results_df.lat), crs="EPSG:4326")

# Load the shapefile
nl_shapefile = gpd.read_file(shapefile_path)

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
nl_shapefile.plot(ax=ax, color='lightgrey', edgecolor='black')

# Create a color normalization between -1 and 1
norm = mcolors.Normalize(vmin=-0.41, vmax=1)

# Plot the data
gdf.plot(column='kge', ax=ax, legend=True, cmap='turbo', markersize=50, norm=norm, legend_kwds={'orientation': "horizontal"})

plt.title('KGE Analysis of Groundwater Levels in the Top Layer')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

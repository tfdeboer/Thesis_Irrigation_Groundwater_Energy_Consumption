import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Define file paths
results_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/output/kge_results/kge_top_layer_results_cor_bias_var.csv'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'

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
fig, ax = plt.subplots(1, 1, figsize=(14, 14))
nl_shapefile.plot(ax=ax, color='lightgrey', edgecolor='black')

# Create a color normalization between -1 and 1
norm = mcolors.Normalize(vmin=-0.41, vmax=1)

# Parameter instellingen
marker_size = 62  # Pas de grootte van de vierkantjes hier aan
marker_shape = 's'  # 'o' voor cirkels, 's' voor vierkantjes, '^' voor driehoekjes, enz.

# Pas de tekstgroottes aan
title_fontsize = 22
label_fontsize = 16
tick_fontsize = 16
legend_title_fontsize = 16  # Lettergrootte van de titel van de legenda
legend_label_fontsize = 16  # Lettergrootte van de schaalgetallen

# Plot de data met aangepaste marker vorm en grootte
plot = gdf.plot(
    column='kge', 
    ax=ax, 
    cmap='seismic', 
    markersize=marker_size, 
    marker=marker_shape, 
    norm=norm
)

# Pas titels en labels aan met specifieke lettergrootte
plt.title('KGE Analysis of Groundwater Levels \nin the Top Layer', fontsize=title_fontsize)
plt.xlabel('Longitude', fontsize=label_fontsize)
plt.ylabel('Latitude', fontsize=label_fontsize)

# Pas de grootte van de ticks (gradenlabels) aan
ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)

# Legenda aan de rechterkant plaatsen
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.00001)  # Plaats de colorbar aan de rechterkant van de plot , pad=0.01
sm = plt.cm.ScalarMappable(cmap='seismic', norm=norm)
cbar = fig.colorbar(sm, cax=cax, orientation='vertical')

# Legenda aanpassingen
cbar.set_label('KGE Value', fontsize=legend_title_fontsize)  # Titel van de legenda
cbar.ax.tick_params(labelsize=legend_label_fontsize)  # Schaalbalk getallen

# Toon de plot
plt.show()
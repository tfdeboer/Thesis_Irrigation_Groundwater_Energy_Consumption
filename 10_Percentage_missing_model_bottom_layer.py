import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Define file paths
missing_data_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/missing_data_percentages_bottom_1980_2015.csv'
well_locations_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/tables/Model_GLOBGM/GLOBGM_Well_data_and_locations/well_locations_bottom_mapping.csv'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'

# Parameters voor visualisatie-instellingen
title_font_size = 24  # Lettergrootte van de titel
axis_label_font_size = 20  # Lettergrootte van de aslabels
tick_font_size = 16  # Lettergrootte van de x- en y-as getallen
colorbar_label_size = 18  # Lettergrootte van het kleurenschaallabel
colorbar_tick_size = 16  # Lettergrootte voor de getallen op de kleurenschaal
marker_size = 70  # Grootte van de markers

# Load the missing data percentages
missing_data_df = pd.read_csv(missing_data_file)

# Extract the pixel number from the filename and convert to int
missing_data_df['pixel_id'] = missing_data_df['File'].str.extract(r'(\d+)').astype(int)

# Load the well locations
well_locations_df = pd.read_csv(well_locations_file)

# Extract the numeric part of well_id and convert to int
well_locations_df['well_id'] = well_locations_df['well_id'].str.extract(r'(\d+)').astype(int)

# Merge the missing data percentages with the well locations
merged_df = pd.merge(missing_data_df, well_locations_df, left_on='pixel_id', right_on='well_id', how='left')

# Create a GeoDataFrame from the merged data
gdf = gpd.GeoDataFrame(merged_df, geometry=gpd.points_from_xy(merged_df.lon, merged_df.lat), crs="EPSG:4326")

# Load the shapefile
nl_shapefile = gpd.read_file(shapefile_path)

# Define the colormap
cmap = plt.get_cmap('seismic')  # or 'cividis' 'seismic'

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(14, 12))  # Verander de figuurafmetingen voor betere leesbaarheid
nl_shapefile.plot(ax=ax, color='lightgrey', edgecolor='black')
gdf.plot(column='MissingDataPercentage', ax=ax, legend=False, cmap=cmap, markersize=marker_size, marker='s')

# Pas de titel en labels aan met grotere tekstgrootte
plt.title('Bottom Layer', fontsize=title_font_size, pad=20) #Percentage of Missing Data in Groundwater Levels \nper Pixel (1980-2015) for the 
plt.xlabel('Longitude', fontsize=axis_label_font_size)
plt.ylabel('Latitude', fontsize=axis_label_font_size)

# Pas de grootte van de ticks (as-getallen) aan
ax.tick_params(axis='both', which='major', labelsize=tick_font_size)

# Kleurenschaal instellen met aangepaste label- en tick-groottes
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=100))
sm._A = []  # Nodig om de colorbar goed te initialiseren
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Percentage of Missing Data %', fontsize=colorbar_label_size)  # Tekst van de kleurenschaal
cbar.ax.tick_params(labelsize=colorbar_tick_size)  # Grootte van de ticks op de kleurenschaal

# Toon de plot
plt.show()
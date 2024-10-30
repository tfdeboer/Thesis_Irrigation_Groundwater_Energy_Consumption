import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec

# File paths voor beide lagen
top_layer_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/missing_data_percentages_top_1980_2015.csv'
bottom_layer_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/missing_data_percentages_bottom_1980_2015.csv'
well_locations_top = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/tables/Model_GLOBGM/GLOBGM_Well_data_and_locations/well_locations_top_mapping.csv'
well_locations_bottom = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/tables/Model_GLOBGM/GLOBGM_Well_data_and_locations/well_locations_bottom_mapping.csv'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'

# Parameters voor visualisatie-instellingen
title_font_size = 24  # Lettergrootte van de titel
axis_label_font_size = 20  # Lettergrootte van de aslabels
tick_font_size = 16  # Lettergrootte van de x- en y-as getallen
colorbar_label_size = 18  # Lettergrootte van het kleurenschaallabel
colorbar_tick_size = 16  # Lettergrootte voor de getallen op de kleurenschaal
marker_size = 70  # Grootte van de markers
suptitle_font_size = 28  # Lettergrootte voor de overkoepelende titel

# Functie om GeoDataFrame voor elke laag te maken
def create_geodataframe(missing_data_file, well_locations_file):
    missing_data_df = pd.read_csv(missing_data_file)
    missing_data_df['pixel_id'] = missing_data_df['File'].str.extract(r'(\d+)').astype(int)
    well_locations_df = pd.read_csv(well_locations_file)
    well_locations_df['well_id'] = well_locations_df['well_id'].str.extract(r'(\d+)').astype(int)
    merged_df = pd.merge(missing_data_df, well_locations_df, left_on='pixel_id', right_on='well_id', how='left')
    gdf = gpd.GeoDataFrame(merged_df, geometry=gpd.points_from_xy(merged_df.lon, merged_df.lat), crs="EPSG:4326")
    return gdf

# Maak GeoDataFrames voor de top- en bottom layer
gdf_top = create_geodataframe(top_layer_file, well_locations_top)
gdf_bottom = create_geodataframe(bottom_layer_file, well_locations_bottom)

# Laad de shapefile van Nederland
nl_shapefile = gpd.read_file(shapefile_path)

# Definieer het kleurenpalet en de schaal voor de kleurenschaal
cmap = plt.get_cmap('seismic')
norm = plt.Normalize(vmin=0, vmax=100)

# Stel de figuur en de layout in met GridSpec
fig = plt.figure(constrained_layout=False, figsize=(30, 15))  # Verhoogde hoogte voor overkoepelende titel en schaalbalk
gs = GridSpec(3, 2, figure=fig, height_ratios=[0.02, 0.5, 0.05])  # Verlaag bovenste rij, verhoog onderste rij

# Overkoepelende titel bovenaan met aangepaste y-positie
fig.suptitle('Comparison of Missing Data Percentages for Top and Bottom Layers', fontsize=suptitle_font_size, weight='bold', y=0.96)

# Subplot voor Top Layer
ax1 = fig.add_subplot(gs[1, 0])
nl_shapefile.plot(ax=ax1, color='lightgrey', edgecolor='black')
gdf_top.plot(column='MissingDataPercentage', ax=ax1, legend=False, cmap=cmap, markersize=marker_size, marker='s')
ax1.set_title('Top Layer', fontsize=title_font_size, pad=10)  # Verklein de pad-waarde voor titelafstand
ax1.set_xlabel('Longitude', fontsize=axis_label_font_size)
ax1.set_ylabel('Latitude', fontsize=axis_label_font_size)
ax1.tick_params(axis='both', which='major', labelsize=tick_font_size)

# Subplot voor Bottom Layer
ax2 = fig.add_subplot(gs[1, 1])
nl_shapefile.plot(ax=ax2, color='lightgrey', edgecolor='black')
gdf_bottom.plot(column='MissingDataPercentage', ax=ax2, legend=False, cmap=cmap, markersize=marker_size, marker='s')
ax2.set_title('Bottom Layer', fontsize=title_font_size, pad=10)  # Verklein de pad-waarde voor titelafstand
ax2.set_xlabel('Longitude', fontsize=axis_label_font_size)
ax2.set_ylabel('')  # Geen y-aslabel voor de tweede plot
ax2.tick_params(axis='both', which='major', labelsize=tick_font_size)

# Voeg een gedeelde horizontale kleurenschaal toe aan de onderkant van beide plots
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm._A = []  # Nodig om de colorbar goed te initialiseren
cbar_ax = fig.add_subplot(gs[2, :])  # Voeg colorbar onderaan de figuur toe
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
cbar.set_label('Percentage of Missing Data %', fontsize=colorbar_label_size)  # Tekst van de kleurenschaal
cbar.ax.tick_params(labelsize=colorbar_tick_size)  # Grootte van de ticks op de kleurenschaal

# Toon de gecombineerde plot
plt.show()
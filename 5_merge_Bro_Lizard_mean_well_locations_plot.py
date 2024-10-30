import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pyproj import Transformer

# Bestandspaden
mean_value_file_1 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/mean_value_per_well/mean_value_per_well.csv'
location_file_1 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/location_and_tubenumbers/location_and_tubenumbers.csv'
timeseries_dir_2 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_Monthly_Mean_GLD_well'
location_file_2 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/GLD_Well_ID_Location.csv'
shapefile = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'

# Parameters voor visualisatie-instellingen
circle_size = 5  # Pas de cirkelgrootte aan
title_font_size = 26  # Lettergrootte van de titel
axis_label_font_size = 22  # Lettergrootte van de aslabels
tick_font_size = 14  # Lettergrootte van de x- en y-as getallen
colorbar_tick_size = 18  # Lettergrootte voor de getallen op de schaalbalk
legend_label = 'Mean Groundwater Depth [m]'  # Legenda label

# Coördinatentransformatie instellen
transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326", always_xy=True)

def convert_to_wgs84(row):
    """Converteer x, y RD naar lon, lat WGS84."""
    lon, lat = transformer.transform(row['x'], row['y'])
    return pd.Series({'lon': lon, 'lat': lat})

# Functie voor het inladen en verwerken van Dataset 1
def load_process_dataset_1(mean_value_file, location_file):
    mean_df = pd.read_csv(mean_value_file)
    location_df = pd.read_csv(location_file)
    location_df[['lon', 'lat']] = location_df.apply(convert_to_wgs84, axis=1)
    combined_df = pd.merge(location_df, mean_df, on='well_number', how='inner')
    combined_df = combined_df.dropna(subset=['mean_value'])
    gdf = gpd.GeoDataFrame(combined_df, geometry=gpd.points_from_xy(combined_df['lon'], combined_df['lat']), crs="EPSG:4326")
    return gdf

# Functie voor het inladen en verwerken van Dataset 2
def load_process_dataset_2(timeseries_dir, location_file):
    location_df = pd.read_csv(location_file)
    location_df.rename(columns={'well_id': 'well_number'}, inplace=True)
    location_df[['lon', 'lat']] = location_df.apply(convert_to_wgs84, axis=1)
    well_averages = []
    for filename in os.listdir(timeseries_dir):
        if filename.endswith(".csv"):
            well_number = os.path.splitext(filename)[0]
            file_path = os.path.join(timeseries_dir, filename)
            timeseries_df = pd.read_csv(file_path)
            if 'value' in timeseries_df.columns:
                mean_value = timeseries_df['value'].mean()
                well_averages.append({'well_number': well_number, 'mean_value': mean_value})
    mean_df = pd.DataFrame(well_averages)
    combined_df = pd.merge(location_df, mean_df, on='well_number', how='inner')
    combined_df = combined_df.dropna(subset=['mean_value'])
    gdf = gpd.GeoDataFrame(combined_df, geometry=gpd.points_from_xy(combined_df['lon'], combined_df['lat']), crs="EPSG:4326")
    return gdf

# Dataset 1 inladen en verwerken
gdf1 = load_process_dataset_1(mean_value_file_1, location_file_1)

# Dataset 2 inladen en verwerken
gdf2 = load_process_dataset_2(timeseries_dir_2, location_file_2)

# Combineer beide GeoDataFrames
combined_gdf = pd.concat([gdf1, gdf2], ignore_index=True)

# Laad shapefile van de provincies
province_gdf = gpd.read_file(shapefile)

# Plot de gecombineerde kaart
fig, ax = plt.subplots(figsize=(14, 10))  # Grotere figuur voor betere leesbaarheid
province_gdf.plot(ax=ax, color='lightgrey', edgecolor='black')

# Plot de gecombineerde data
vmin, vmax = 0, 50  # Stel een uniforme schaal in voor de gecombineerde dataset
combined_gdf.plot(column='mean_value', cmap='terrain', markersize=circle_size, legend=True, ax=ax, norm=plt.Normalize(vmin=vmin, vmax=vmax))

# Voeg een enkele kleurenbalk toe
sm = plt.cm.ScalarMappable(cmap='terrain', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label(legend_label, fontsize=axis_label_font_size)

# Pas de lettergrootte van de getallen op de kleurenbalk aan
cbar.ax.tick_params(labelsize=colorbar_tick_size)

# Titel en labels instellen
plt.title('Mean Groundwater Depth \nper Well (1980-2015)', fontsize=title_font_size)
plt.xlabel('Longitude', fontsize=axis_label_font_size)
plt.ylabel('Latitude', fontsize=axis_label_font_size)

# Pas de lettergrootte van de tick labels op de assen aan
ax.tick_params(axis='both', which='major', labelsize=tick_font_size)

# Voeg grid toe en visualiseer de kaart
plt.grid(True)
plt.show()
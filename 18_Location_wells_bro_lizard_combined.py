import os
import geopandas as gpd
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from shapely.geometry import Point

# Functie om coördinaten te extraheren
def extract_coordinates(metadata):
    x_coord = None
    y_coord = None
    for line in metadata.splitlines():
        if 'x :' in line:
            x_coord = line.split(':')[1].strip().strip(',').strip("'").strip('"')
        if 'y :' in line:
            y_coord = line.split(':')[1].strip().strip(',').strip("'").strip('"')
    return x_coord, y_coord

# Shapefile pad
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/shp/NL/Netherlands.shp'
netherlands = gpd.read_file(shapefile_path)

# Controleer het coördinatensysteem van de shapefile
print(f"Shapefile CRS: {netherlands.crs}")

# Eerste bron (blauw)
wells_directory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_GLD_well'
well_locations = []

for well_id in os.listdir(wells_directory):
    well_dir = os.path.join(wells_directory, well_id)
    if os.path.isdir(well_dir):
        metadata_path = os.path.join(well_dir, f'gw_bro_{well_id}.txt')
        if os.path.exists(metadata_path):
            try:
                if os.path.getsize(metadata_path) > 0:
                    with open(metadata_path, 'r') as file:
                        metadata = file.read().strip()
                    x_coord, y_coord = extract_coordinates(metadata)
                    if x_coord is not None and y_coord is not None:
                        well_locations.append({
                            'well_id': well_id,
                            'x': float(x_coord),
                            'y': float(y_coord)
                        })
                    else:
                        print(f"Coordinates not found for well {well_id}")
                else:
                    print(f"Metadata bestand is leeg voor well {well_id}")
            except Exception as e:
                print(f"Error processing metadata for well {well_id}: {e}")

if well_locations:
    well_gdf = gpd.GeoDataFrame(
        well_locations, 
        geometry=gpd.points_from_xy(
            [loc['x'] for loc in well_locations], 
            [loc['y'] for loc in well_locations]
        ), 
        crs='EPSG:28992'  # Zorg ervoor dat het coördinatensysteem overeenkomt
    )

    if netherlands.crs != well_gdf.crs:
        netherlands = netherlands.to_crs(well_gdf.crs)

# Tweede bron (rood)
outputDirectory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/'
pklz_file = os.path.join(outputDirectory, 'gw_bro_Netherlands.pklz')

with open(pklz_file, 'rb') as f:
    gw_bro = pickle.load(f)

locations = [{'geometry': Point(row['x'], row['y'])} for index, row in gw_bro.iterrows()]
gdf = gpd.GeoDataFrame(locations, crs='EPSG:28992')
gdf = gdf.to_crs(netherlands.crs)

# Plotten van de shapefile en de well locaties
fig, ax = plt.subplots(figsize=(10, 10))
netherlands.plot(ax=ax, color='lightgrey')

if not well_gdf.empty:
    well_gdf.plot(ax=ax, color='blue', markersize=1, alpha=0.7, label='BRO GLD')

if not gdf.empty:
    gdf.plot(ax=ax, color='red', markersize=1, alpha=0.7, label='Lizard')

# Legenda toevoegen
plt.legend()

# Toon de plot zonder labels
plt.title('Locations of Wells in the Netherlands')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Printen van het aantal locaties
print(f"Number of locations from BRO GLD: {len(well_locations)}")
print(f"Number of locations from Lizard: {len(locations)}")

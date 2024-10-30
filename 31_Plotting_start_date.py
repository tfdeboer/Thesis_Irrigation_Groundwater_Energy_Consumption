import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon

# Pad naar de gegevensbestanden
well_data_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/Lizard_PDOK_all_data_wells_location_depth_missing_value_percentage.csv'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/shp/NL/Netherlands.shp'

# Laad de putgegevens
well_data = pd.read_csv(well_data_path)

# Laad de shapefile
netherlands_gdf = gpd.read_file(shapefile_path)

# Functie om multi-part geometrieën te behandelen
def handle_multiparts(gdf):
    geometries = []
    for geom in gdf.geometry:
        if isinstance(geom, MultiPolygon):
            for part in geom.geoms:
                geometries.append(part)
        else:
            geometries.append(geom)
    return gpd.GeoDataFrame(geometry=geometries, crs=gdf.crs)

# Pas de functie toe om multi-part geometrieën te behandelen
netherlands_gdf = handle_multiparts(netherlands_gdf)

# Controleer en stel de CRS van de shapefile in op EPSG:4326
if netherlands_gdf.crs != "EPSG:4326":
    netherlands_gdf = netherlands_gdf.to_crs(epsg=4326)

# Converteer putgegevens naar GeoDataFrame met CRS EPSG:28992 (Amersfoort / RD New)
well_gdf = gpd.GeoDataFrame(
    well_data, 
    geometry=gpd.points_from_xy(well_data.x, well_data.y),
    crs="EPSG:28992"
)

# Converteer de CRS van de putgegevens naar EPSG:4326
well_gdf = well_gdf.to_crs(epsg=4326)

# Converteer de startdatum naar datetime en dan naar een jaar
well_gdf['time_range_start'] = pd.to_datetime(well_gdf['time_range_start'], errors='coerce')
well_gdf['start_year'] = well_gdf['time_range_start'].dt.year

###### Filter de data om alleen de jaren binnen de range 1958 tot 2015 te behouden #######
well_gdf = well_gdf[(well_gdf['start_year'] >= 1958) & (well_gdf['start_year'] <= 2015)]

# Definieer het kleurenschema gebaseerd op het startjaar
cmap = plt.cm.RdYlGn_r  # Gebruik de kleurenschaal van rood naar groen
norm = plt.Normalize(vmin=1958, vmax=2015)
well_gdf['color'] = well_gdf['start_year'].apply(lambda x: cmap(norm(x)))

# Plot
fig, ax = plt.subplots(figsize=(10, 10))
netherlands_gdf.plot(ax=ax, color='white', edgecolor='black')
well_gdf.plot(ax=ax, color=well_gdf['color'], markersize=2.5, alpha=0.6)

# Voeg een colorbar toe
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Start Year')

plt.title('Start year of wells in the Netherlands (from 1958 to 2015)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

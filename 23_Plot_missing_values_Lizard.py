import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon

# Pad naar de gegevensbestanden
well_data_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/Wells_data_Lizard_1958_2015_locations_missing_value.csv'
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

# Definieer het kleurenschema gebaseerd op missing_percentage
cmap = plt.cm.RdYlGn_r  # Gebruik de omgekeerde kleurenschaal
norm = plt.Normalize(vmin=0, vmax=100)
well_gdf['color'] = well_gdf['missing_percentage'].apply(lambda x: cmap(norm(x)))

# Plot
fig, ax = plt.subplots(figsize=(10, 10))
netherlands_gdf.plot(ax=ax, color='white', edgecolor='black')
well_gdf.plot(ax=ax, color=well_gdf['color'], markersize=10, alpha=0.6)

# Voeg een colorbar toe
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Missing Percentage')

plt.title('Wells in the Netherlands with missing percentage from Lizard')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

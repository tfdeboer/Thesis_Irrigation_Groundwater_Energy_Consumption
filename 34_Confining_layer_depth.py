import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from netCDF4 import Dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import MultiPolygon

# Pad naar het NetCDF-bestand en de shapefile
netcdf_file_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/confining_layer_thickness_5arcmin_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/shp/NL/Netherlands.shp'

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

# Laad de NetCDF gegevens
nc_data = Dataset(netcdf_file_path, mode='r')

# Druk de variabele namen af
print("Available variables in the NetCDF file:")
print(nc_data.variables.keys())

# Controleer of 'thickness_deklaag' een geldige variabele naam is
if 'thickness_deklaag' in nc_data.variables:
    # Lees de variabelen uit het NetCDF-bestand
    lons = nc_data.variables['lon'][:]
    lats = nc_data.variables['lat'][:]
    thickness_deklaag = np.squeeze(nc_data.variables['thickness_deklaag'][:])

    # Maak een meshgrid van de lons en lats voor het plotten
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([3, 8, 50.5, 53.7], crs=ccrs.PlateCarree())

    # Voeg de shapefile toe aan de plot
    netherlands_gdf.boundary.plot(ax=ax, edgecolor='black')

    # Voeg de NetCDF gegevens toe aan de plot
    thickness_plot = ax.pcolormesh(lon_grid, lat_grid, thickness_deklaag, cmap='viridis', transform=ccrs.PlateCarree())

    # Voeg een colorbar toe
    cbar = fig.colorbar(thickness_plot, ax=ax, orientation='vertical', pad=0.02, aspect=50)
    cbar.set_label('Confining Layer Thickness [m]')

    # Voeg extra kaartfuncties toe
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    plt.title('Confining Layer Thickness in the Netherlands')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
else:
    print("The variable 'thickness_deklaag' is not found in the NetCDF file.")

import netCDF4 as nc
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Bestanden laden
nc_file_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/irrGWWW_m3_year_1960_2019_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'

# Laad de shapefile
gdf = gpd.read_file(shapefile_path)

# Laad de NetCDF data
ds = nc.Dataset(nc_file_path)

# Verondersteld dat de NetCDF variabele 'irrigation_withdrawal' heet
irrigation_withdrawal = ds.variables['irrigation_withdrawal'][:]
lat = ds.variables['lat'][:]
lon = ds.variables['lon'][:]
time = nc.num2date(ds.variables['time'][:], units=ds.variables['time'].units)

# Tijd-index berekenen voor de periode 1980-2015
start_year = 1980
end_year = 2015
years = np.array([t.year for t in time])

# Filter de data voor de gewenste periode
year_mask = (years >= start_year) & (years <= end_year)
irrigation_withdrawal = irrigation_withdrawal[year_mask, :, :, :]  # Selecteer alleen de gewenste jaren
years = years[year_mask]

# Maak per jaar een plot van de grondwateropname voor irrigatie
for i, year in enumerate(years):
    # Bereken de gemiddelde irrigatieopname voor het huidige jaar en verwijder overbodige dimensie
    yearly_irrigation = np.squeeze(irrigation_withdrawal[i, :, :, 0])  # Verwijder de overbodige dimensie met squeeze

    # Creëer een figuur met de shapefile en de irrigatiegegevens voor het huidige jaar
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})

    # Voeg de shapefile grenzen toe aan de plot
    gdf.plot(ax=ax, edgecolor='black', facecolor='none')

    # Creëer een raster voor de lat/lon van het NetCDF-bestand
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    # Plot de irrigatiegegevens als een rasterlaag
    c = ax.pcolormesh(lon_grid, lat_grid, yearly_irrigation, cmap='BuPu', shading='auto', vmin=0, vmax=1000)

    # Colorbar toevoegen met de schaalbalk
    cbar = plt.colorbar(c, ax=ax, orientation='horizontal', pad=0.05, label=f'Groundwater Withdrawal [m³] in {year}')
    cbar.ax.tick_params(labelsize=12)

    # Titel en labels instellen
    ax.set_title(f'Groundwater Withdrawal for Irrigation [m³] in {year}', fontsize=16)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    # Voeg gridlijnen toe voor een duidelijker overzicht
    ax.gridlines(draw_labels=True, linestyle="--", linewidth=0.5, color='gray')

    # Toon de plot voor het huidige jaar
    plt.tight_layout()
    plt.show()
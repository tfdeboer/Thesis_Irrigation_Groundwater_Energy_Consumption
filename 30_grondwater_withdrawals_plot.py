import netCDF4 as nc
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib import ticker

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

# Spiegel de latitude-array om correct te plotten
lat_flipped = lat[::-1]

# Controleer of de latitude correct is gespiegeld
print(f"Originele latitude (eerste 5 waarden): {lat[:5]}")
print(f"Gespiegelde latitude (eerste 5 waarden): {lat_flipped[:5]}")

# Tijd-index berekenen voor de periode 1980-2015
start_year = 1980
end_year = 2015
years = np.array([t.year for t in time])

start_idx = np.where(years == start_year)[0][0]
end_idx = np.where(years == end_year)[0][-1]

# Gemiddelde grondwateropname voor irrigatie per pixel over de periode 1980-2015 berekenen
average_irrigation_withdrawal = np.mean(irrigation_withdrawal[start_idx:end_idx + 1, :, :], axis=0)

# Zorg dat de array correct is qua dimensie en spiegel de data als lat gespiegeld is
average_irrigation_withdrawal = np.squeeze(average_irrigation_withdrawal[::-1, :])  # Spiegel de rasterdata en verwijder extra dimensie

# Controleer de afmetingen en een voorbeeld van de data
print(f"Afmetingen van de gemiddelde opname data: {average_irrigation_withdrawal.shape}")
print(f"Voorbeeld van gespiegelde data (eerste 5 rijen):\n{average_irrigation_withdrawal[:5, :]}")

# Plotting: de shapefile en de gemiddelde grondwateropname voor irrigatie
fig, ax = plt.subplots(figsize=(10, 10))

# Plot de shapefile
gdf.boundary.plot(ax=ax, linewidth=1, color='black')

# Creëer een raster voor de gespiegelde lat/lon van het NetCDF-bestand
lon_grid, lat_grid = np.meshgrid(lon, lat_flipped)

# Plot de gemiddelde grondwateropname voor irrigatie als een rasterlaag
c = ax.pcolormesh(lon_grid, lat_grid, average_irrigation_withdrawal, cmap='BuPu', shading='auto')

# Colorbar aanpassen met aangepaste notatie voor duizendtallen
cbar = plt.colorbar(c, ax=ax, format=ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
cbar.set_label('Groundwater Withdrawal [m³]')

# Titel en labels
plt.title('Average Groundwater Withdrawal for Irrigation [m³] (1980-2015)', fontsize=18)
plt.xlabel('Longitude', fontsize=14)
plt.ylabel('Latitude', fontsize=14)

# Pas de labels op de assen aan voor grotere tekst
ax.tick_params(axis='both', which='major', labelsize=12)

# Plot weergeven
plt.tight_layout()
plt.show()

# Sla de gemiddelde grondwateropname voor irrigatie op in een Pandas DataFrame
df = pd.DataFrame({
    'Latitude': lat_grid.flatten(),
    'Longitude': lon_grid.flatten(),
    'Average_Irrigation_Withdrawal': average_irrigation_withdrawal.flatten()
})

# Sla het DataFrame op als CSV
output_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/average_irrigation_withdrawal_1980_2015_per_pixel.csv'
df.to_csv(output_path, index=False)

print(f"De gemiddelde grondwateropname voor irrigatie per pixel is opgeslagen in het DataFrame op {output_path}.")
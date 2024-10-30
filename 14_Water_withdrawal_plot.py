import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase

# Paden naar de bestanden
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/data/shp/NL/Netherlands.shp'
# all years:
#netcdf_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/data/nc/NL/irrigationWaterWithdrawal_global_yearly-total_1960_2019_basetier1_NL.nc'

# trend (helling):
netcdf_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/data/nc/NL/trend_irrigationWaterWithdrawal_global_yearly-total_1960_2019_basetier1_NL_trend.nc'

# Mean value:
# netcdf_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/data/nc/NL/mean_irrigationWaterWithdrawal_global_yearly_1960_2019.nc'

# Laad de shapefile
shapefile = gpd.read_file(shapefile_path)

# Laad de NetCDF data
dataset = Dataset(netcdf_path)
variable_name = 'irrigation_withdrawal'  
water_withdrawal = dataset.variables[variable_name][:]

# Stel de projectie in voor de plot
fig, ax = plt.subplots(figsize=(10, 10))
shapefile.boundary.plot(ax=ax)

# Veronderstel dat je de water_withdrawal data wilt visualiseren voor een specifiek jaar
# Vervang de index met het gewenste jaar
year_index = 0  # Index voor het gewenste jaar, bijvoorbeeld 0 voor het eerste jaar in de dataset

# Veronderstel dat de NetCDF data in dezelfde projectie als de shapefile is
# Hier gaan we ervan uit dat de water_withdrawal data een 2D array is die overeenkomt met de shapefile
water_withdrawal_data = water_withdrawal[year_index, :, :]

# Stel de normalisatie in zodat de schaalbalk begint bij 0 (bij plotten van waterwithdrawal, niet bij trend)
# norm = Normalize(vmin=0, vmax=np.nanmax(water_withdrawal_data))

# Plot de data over de shapefile
# Voeg ', norm=norm' toe als er een waterwitdrawal wordt geplot zodat de as bij 0 begint!!!!
im = ax.imshow(water_withdrawal_data, cmap='viridis', extent=[shapefile.total_bounds[0], shapefile.total_bounds[2], shapefile.total_bounds[1], shapefile.total_bounds[3]], alpha=0.6)

# Voeg een schaalbalk toe
cbar = plt.colorbar(im, ax=ax, orientation='vertical')
cbar.set_label('Water Withdrawal (m^3)')  

plt.title('Water Withdrawal Trends for the Netherlands')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Sluit de NetCDF dataset
dataset.close()

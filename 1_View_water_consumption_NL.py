import netCDF4 as nc
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# Define file paths
nc_file_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/irrGWWW_m3_year_1960_2019_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/shp/NL/Netherlands.shp'

# Load the shapefile
gdf = gpd.read_file(shapefile_path)

# Load the NetCDF file
ds = nc.Dataset(nc_file_path)

# Explore the dimensions and variables to understand the data
print(ds)
print(ds.variables.keys())

# Use the correct variable name 'irrigation_withdrawal'
data = ds.variables['irrigation_withdrawal'][:]  # This is the correct variable name
lat = ds.variables['lat'][:]
lon = ds.variables['lon'][:]

# Assume we want to plot data for a specific year, for example, 2019
# The 'time' dimension represents years, adjust the index accordingly
data_2019 = data[-1, :, :, 0]  # The last time index might correspond to 2019, adjust as needed

# Create a meshgrid for the coordinates
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.plot(ax=ax, color='none', edgecolor='black')

# Overlay the water withdrawal data
c = ax.pcolormesh(lon_grid, lat_grid, data_2019, cmap='Blues', shading='auto')
plt.colorbar(c, ax=ax, label='Water Withdrawal (m3/year)')

# Set the title and labels
plt.title('Water Withdrawal in the Netherlands (2019)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Display the plot
plt.show()

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
data = ds.variables['irrigation_withdrawal'][:]  # Assuming this is the correct variable name
lat = ds.variables['lat'][:]
lon = ds.variables['lon'][:]
time = ds.variables['time'][:]  # Assuming 'time' is the correct dimension for years

# Determine the correct indices for the years 1980 and 2015
def get_time_index(year):
    start_year = 1960  # Assuming time starts from 1960
    return int(year - start_year)

start_year = 1980
end_year = 2015

start_index = get_time_index(start_year)
end_index = get_time_index(end_year)

# Calculate the average over the selected years
average_data = np.mean(data[start_index:end_index+1, :, :, 0], axis=0)

# Create a meshgrid for the coordinates
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.plot(ax=ax, color='none', edgecolor='black')

# Overlay the average water withdrawal data
c = ax.pcolormesh(lon_grid, lat_grid, average_data, cmap='Blues', shading='auto')
plt.colorbar(c, ax=ax, label='Average Water Withdrawal (m3/year)')

# Set the title and labels
plt.title('Average Water Withdrawal in the Netherlands (1980-2015)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Display the plot
plt.show()

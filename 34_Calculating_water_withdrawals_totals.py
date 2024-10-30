import netCDF4 as nc
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # Voor het opslaan van de data in een CSV-bestand

# Define file paths
nc_file_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/irrGWWW_m3_year_1960_2019_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/shp/NL/Netherlands.shp'
output_csv_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/output/total_groundwater_withdrawal.csv'

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
time = ds.variables['time'][:]

# Bereken het totale grondwaterverbruik per jaar (m³/year)
total_withdrawal_per_year = []

for i in range(data.shape[0]):  # Loop over alle jaren
    yearly_data = data[i, :, :, 0]  # Verwijder overbodige dimensies
    total_withdrawal = np.nansum(yearly_data)  # Som van alle gridcellen, NaN's negeren
    total_withdrawal_per_year.append(total_withdrawal)

# Maak een Pandas DataFrame voor overzichtelijkheid en om naar CSV op te slaan
df_withdrawal = pd.DataFrame({
    'Year': np.arange(1960, 1960 + len(total_withdrawal_per_year)),  # Aannemende dat de data van 1960 tot 2019 loopt
    'Total_Withdrawal_m3': total_withdrawal_per_year  # In m³ per jaar
})

# Sla de resultaten op naar een CSV-bestand
df_withdrawal.to_csv(output_csv_path, index=False)
print(f'Total groundwater withdrawal per year saved to: {output_csv_path}')

# Optional: Plot water withdrawal for a specific year (e.g., 2019)
data_2019 = data[-1, :, :, 0]  # De laatste tijdsindex voor 2019

# Create a meshgrid for the coordinates
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.plot(ax=ax, color='none', edgecolor='black')

# Overlay the water withdrawal data
c = ax.pcolormesh(lon_grid, lat_grid, data_2019, cmap='Blues', shading='auto')
plt.colorbar(c, ax=ax, label='Water Withdrawal (m³/year)')

# Set the title and labels
plt.title('Water Withdrawal in the Netherlands (2019)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Display the plot
plt.show()
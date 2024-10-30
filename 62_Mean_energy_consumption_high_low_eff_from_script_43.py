import netCDF4 as nc
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Constants
g = 9.8  # gravity [m/s^2]
rho = 1000  # density of water [kg/m^3]
conversion_factor = 3.6e6  # to convert J to kWh
dt = 365 * 24 * 3600  # seconds in a year
pump_efficiency_low = 0.4  # lower pump efficiency
pump_efficiency_high = 0.7  # higher pump efficiency

# File paths
groundwater_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/globgm_top_5arcmin_monthly_1958_2015_netherlands.nc'
withdrawal_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/irrGWWW_m3_year_1960_2019_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'

# Load the shapefile
gdf = gpd.read_file(shapefile_path)

# Load the groundwater data (monthly data)
groundwater_ds = nc.Dataset(groundwater_file)
groundwater_depth = groundwater_ds.variables['groundwater_depth'][:]  # Assuming this is the variable
time_groundwater = nc.num2date(groundwater_ds.variables['time'][:], units=groundwater_ds.variables['time'].units)

# Load the water withdrawal data (yearly data)
withdrawal_ds = nc.Dataset(withdrawal_file)
water_withdrawal = withdrawal_ds.variables['irrigation_withdrawal'][:]  # Assuming this is the variable
time_withdrawal = nc.num2date(withdrawal_ds.variables['time'][:], units=withdrawal_ds.variables['time'].units)

# Extract years from the time variables
years_groundwater = np.array([dt.year for dt in time_groundwater])
years_withdrawal = np.array([dt.year for dt in time_withdrawal])

# Get the unique years for both datasets
unique_years_groundwater = np.unique(years_groundwater)
unique_years_withdrawal = np.unique(years_withdrawal)

# Initialize arrays to store energy consumption per pixel
energy_low_efficiency_map = np.zeros_like(groundwater_depth[0, :, :, 0])
energy_high_efficiency_map = np.zeros_like(groundwater_depth[0, :, :, 0])
count_years = 0

# Function to calculate energy consumption
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency) #* 1e-9  # Convert to TWh
    return energy

# Loop over the years 1980–2015 and accumulate energy maps
for year in range(1980, 2016):
    if year in unique_years_groundwater and year in unique_years_withdrawal:
        # Get groundwater data for the current year
        year_mask_groundwater = years_groundwater == year
        yearly_data = groundwater_depth[year_mask_groundwater, :, :, 0]  # Select all months for the year, ignore unnecessary dimension

        # Calculate mean over all months per pixel for the year
        yearly_mean_per_pixel = np.nanmean(yearly_data, axis=0)  # Mean over months for each pixel

        # Get water withdrawal data for the corresponding year
        year_index_withdrawal = np.where(years_withdrawal == year)[0][0]
        Q = np.squeeze(water_withdrawal[year_index_withdrawal, :, :, 0])  # Water withdrawal for the year

        # Ensure the shape matches
        if yearly_mean_per_pixel.shape != Q.shape:
            raise ValueError(f"Shape mismatch: Groundwater shape {yearly_mean_per_pixel.shape}, Water withdrawal shape {Q.shape}")
        
        # Calculate energy per pixel for both low and high pump efficiency
        energy_map_low = calculate_energy(yearly_mean_per_pixel, Q, pump_efficiency_low)
        energy_map_high = calculate_energy(yearly_mean_per_pixel, Q, pump_efficiency_high)

        # Accumulate energy maps
        energy_low_efficiency_map += energy_map_low
        energy_high_efficiency_map += energy_map_high
        count_years += 1

# Average the energy maps over the years
energy_low_efficiency_map /= count_years
energy_high_efficiency_map /= count_years

# Plotting: low efficiency
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the shapefile
gdf.boundary.plot(ax=ax, linewidth=1, color='black')

# Plot the average energy consumption map (low efficiency)
lon = groundwater_ds.variables['lon'][:]
lat = groundwater_ds.variables['lat'][:]
lon_grid, lat_grid = np.meshgrid(lon, lat)

c = ax.pcolormesh(lon_grid, lat_grid, energy_low_efficiency_map, cmap='viridis', shading='auto', norm=LogNorm())
plt.colorbar(c, ax=ax, label='Average Energy Consumption (TWh) - Low Efficiency')

plt.title('Average Energy Consumption (1980-2015) for Groundwater Pumping in the Netherlands (Low Efficiency)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.show()

# Plotting: high efficiency
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the shapefile
gdf.boundary.plot(ax=ax, linewidth=1, color='black')

# Plot the average energy consumption map (high efficiency)
c = ax.pcolormesh(lon_grid, lat_grid, energy_high_efficiency_map, cmap='PuOr', shading='auto', norm=LogNorm())
plt.colorbar(c, ax=ax, label='Average Energy Consumption (TWh) - High Efficiency')

plt.title('Average Energy Consumption (1980-2015) for Groundwater Pumping in the Netherlands (High Efficiency)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.show()

# Saving average values to a DataFrame
df_low = pd.DataFrame({
    'Latitude': lat_grid.flatten(),
    'Longitude': lon_grid.flatten(),
    'Average_Energy_Consumption_Low': energy_low_efficiency_map.flatten()
})

df_high = pd.DataFrame({
    'Latitude': lat_grid.flatten(),
    'Longitude': lon_grid.flatten(),
    'Average_Energy_Consumption_High': energy_high_efficiency_map.flatten()
})

# Save the DataFrames (optional)
df_low.to_csv('/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/average_energy_low_efficiency_1980_2015.csv', index=False)
df_high.to_csv('/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/average_energy_high_efficiency_1980_2015.csv', index=False)
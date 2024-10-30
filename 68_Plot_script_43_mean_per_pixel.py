import netCDF4 as nc
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

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

# Synchronize the period between 1980 and 2015
start_year = 1980
end_year = 2015

# Indices for the synchronized period
year_indices_groundwater = np.where((years_groundwater >= start_year) & (years_groundwater <= end_year))[0]
year_indices_withdrawal = np.where((years_withdrawal >= start_year) & (years_withdrawal <= end_year))[0]

# Initialize arrays to accumulate energy consumption
accumulated_energy_low = np.zeros_like(groundwater_depth[0, :, :, 0])
accumulated_energy_high = np.zeros_like(groundwater_depth[0, :, :, 0])
valid_pixel_counts = np.zeros_like(groundwater_depth[0, :, :, 0])

# Function to calculate energy consumption
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency)  # Convert to kWh
    return energy

# Loop over each year between 1980 and 2015
for idx_groundwater, idx_withdrawal in zip(year_indices_groundwater, year_indices_withdrawal):
    groundwater_depth_year = groundwater_depth[idx_groundwater, :, :, 0]  # Use the first layer (0)
    water_withdrawal_year = water_withdrawal[idx_withdrawal, :, :, 0]

    # Apply mask to handle NaN values carefully
    valid_mask = (~np.isnan(groundwater_depth_year)) & (~np.isnan(water_withdrawal_year))

    if not valid_mask.any():
        continue  # Skip if there's no valid data

    # Calculate energy consumption for low and high pump efficiency
    energy_low = np.zeros_like(groundwater_depth_year)
    energy_high = np.zeros_like(groundwater_depth_year)
    
    energy_low[valid_mask] = calculate_energy(groundwater_depth_year[valid_mask], water_withdrawal_year[valid_mask], pump_efficiency_low)
    energy_high[valid_mask] = calculate_energy(groundwater_depth_year[valid_mask], water_withdrawal_year[valid_mask], pump_efficiency_high)

    # Accumulate energy consumption over the years (sum of energy per year)
    accumulated_energy_low += energy_low
    accumulated_energy_high += energy_high

    # Count valid pixels (where data is available)
    valid_pixel_counts += valid_mask

# Avoid division by zero for pixels with no valid data
valid_pixel_counts[valid_pixel_counts == 0] = np.nan

# Calculate the average energy consumption per pixel over the period
average_energy_low = accumulated_energy_low / valid_pixel_counts
average_energy_high = accumulated_energy_high / valid_pixel_counts

# Prepare for plotting the average energy consumption (1980-2015)
lon = groundwater_ds.variables['lon'][:]
lat = groundwater_ds.variables['lat'][:]
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Plot the average energy consumption for low efficiency
fig, ax = plt.subplots(figsize=(10, 10))
gdf.boundary.plot(ax=ax, linewidth=1, color='black')
c = ax.pcolormesh(lon_grid, lat_grid, average_energy_low, cmap='viridis', shading='auto')
plt.colorbar(c, ax=ax, label='Average Energy Consumption (kWh) - Low Efficiency (1980-2015)')
plt.title('Average Energy Consumption for Groundwater Pumping in the Netherlands (1980-2015, Low Efficiency)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
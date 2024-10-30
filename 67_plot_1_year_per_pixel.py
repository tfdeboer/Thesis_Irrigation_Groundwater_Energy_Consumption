import netCDF4 as nc
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# File paths (updated to match the provided dataset paths)
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

# Constants for energy calculation
g = 9.8  # gravity [m/s^2]
rho = 1000  # density of water [kg/m^3]
conversion_factor = 3.6e6  # to convert J to kWh
dt = 365 * 24 * 3600  # seconds in a year
pump_efficiency_low = 0.4  # lower pump efficiency
pump_efficiency_high = 0.7  # higher pump efficiency

# Specify the year you want to plot
year_to_plot = 1983  # Change this year as needed

# Extract years from the time variables
years_groundwater = np.array([t.year for t in time_groundwater])
years_withdrawal = np.array([t.year for t in time_withdrawal])

# Find the index of the selected year in the datasets
year_idx_groundwater = np.where(years_groundwater == year_to_plot)[0]
year_idx_withdrawal = np.where(years_withdrawal == year_to_plot)[0]

# Ensure we found data for the selected year
if len(year_idx_groundwater) == 0 or len(year_idx_withdrawal) == 0:
    raise ValueError(f"No data found for the selected year: {year_to_plot}")

# Get groundwater depth and water withdrawal for the selected year
groundwater_depth_year = np.mean(groundwater_depth[year_idx_groundwater, :, :], axis=0)  # Mean over months
water_withdrawal_year = water_withdrawal[year_idx_withdrawal, :, :]

# Function to calculate energy consumption
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency)  # Convert to kWh
    return energy

# Calculate energy consumption for both low and high pump efficiencies for the selected year
energy_low_efficiency = calculate_energy(groundwater_depth_year, water_withdrawal_year, pump_efficiency_low)
energy_high_efficiency = calculate_energy(groundwater_depth_year, water_withdrawal_year, pump_efficiency_high)

# Prepare for plotting
lon = groundwater_ds.variables['lon'][:]
lat = groundwater_ds.variables['lat'][:]
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Plot energy consumption with low efficiency
fig, ax = plt.subplots(figsize=(10, 10))
gdf.boundary.plot(ax=ax, linewidth=1, color='black')
c = ax.pcolormesh(lon_grid, lat_grid, np.squeeze(energy_low_efficiency), cmap='viridis', shading='auto')
plt.colorbar(c, ax=ax, label='Energy Consumption (kWh) - Low Efficiency')
plt.title(f'Energy Consumption ({year_to_plot}) for Groundwater Pumping in the Netherlands (Low Efficiency)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Plot energy consumption with high efficiency
fig, ax = plt.subplots(figsize=(10, 10))
gdf.boundary.plot(ax=ax, linewidth=1, color='black')
c = ax.pcolormesh(lon_grid, lat_grid, np.squeeze(energy_high_efficiency), cmap='viridis', shading='auto')
plt.colorbar(c, ax=ax, label='Energy Consumption (kWh) - High Efficiency')
plt.title(f'Energy Consumption ({year_to_plot}) for Groundwater Pumping in the Netherlands (High Efficiency)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Save energy consumption results in a DataFrame
df = gpd.DataFrame({
    'Latitude': lat_grid.flatten(),
    'Longitude': lon_grid.flatten(),
    'Energy_Low_Efficiency_kWh': energy_low_efficiency.flatten(),
    'Energy_High_Efficiency_kWh': energy_high_efficiency.flatten()
})

# Save the DataFrame to a CSV file
output_file_path = f'/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/energy_consumption_map_Chatgpt_{year_to_plot}.csv'
df.to_csv(output_file_path, index=False)

print(f"Data saved to {output_file_path}")
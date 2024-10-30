import netCDF4 as nc
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.8  # gravity [m/s^2]
rho = 1000  # density of water [kg/m^3]
eta_min = 0.4  # minimum pump efficiency
eta_max = 0.7  # maximum pump efficiency
conversion_factor = 3.6e6  # to convert J to kWh

# File paths
groundwater_nc_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/globgm_top_5arcmin_monthly_1958_2015_netherlands.nc'
water_withdrawal_nc_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/irrGWWW_m3_year_1960_2019_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/shp/NL/Netherlands.shp'


# Load the shapefile
gdf = gpd.read_file(shapefile_path)

# Load the groundwater data
groundwater_ds = nc.Dataset(groundwater_nc_path)
groundwater_depth = groundwater_ds.variables['groundwater_depth'][:]  # Adjust this to match the actual variable name
time_groundwater = nc.num2date(groundwater_ds.variables['time'][:], units=groundwater_ds.variables['time'].units)

# Calculate annual average groundwater depth (H) from monthly data
years = np.arange(1980, 2016)
annual_groundwater_depth = np.zeros((len(years), groundwater_depth.shape[1], groundwater_depth.shape[2]))

for i, year in enumerate(years):
    # Convert the times to datetime objects and filter by year
    mask = np.array([dt.year == year for dt in time_groundwater])
    yearly_data = np.mean(groundwater_depth[mask], axis=0)
    
    # Remove any singleton dimensions
    yearly_data = np.squeeze(yearly_data)
    
    # Assign to the annual array
    annual_groundwater_depth[i] = yearly_data

# Load the water withdrawal data
water_withdrawal_ds = nc.Dataset(water_withdrawal_nc_path)
water_withdrawal = water_withdrawal_ds.variables['irrigation_withdrawal'][:]
time_water_withdrawal = nc.num2date(water_withdrawal_ds.variables['time'][:], units=water_withdrawal_ds.variables['time'].units)

# Calculate the energy required to pump groundwater per year
energy_min = np.zeros((len(years), water_withdrawal.shape[1], water_withdrawal.shape[2]))
energy_max = np.zeros((len(years), water_withdrawal.shape[1], water_withdrawal.shape[2]))

for i, year in enumerate(years):
    H = annual_groundwater_depth[i]
    Q = np.squeeze(water_withdrawal[i])  # Remove the singleton dimension from Q if it exists
    dt = 365 * 24 * 3600  # Time in seconds per year

    # Ensure H and Q have the same shape
    if H.shape != Q.shape:
        raise ValueError(f"Shape mismatch: H shape {H.shape}, Q shape {Q.shape}")
    
    energy_min[i] = (g * H * rho * Q * dt) / (conversion_factor * eta_min)
    energy_max[i] = (g * H * rho * Q * dt) / (conversion_factor * eta_max)

# Convert energy to TWh for easier interpretation
energy_min_twh = energy_min / 1e9
energy_max_twh = energy_max / 1e9

# Plotting the energy use for a selected year (e.g., 2015)
year_index = -1  # Index for 2015, adjust if necessary

# Plot only the minimum energy use
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.plot(ax=ax, color='none', edgecolor='black')

# Plot min energy consumption for 2015
c_min = ax.pcolormesh(water_withdrawal_ds.variables['lon'][:], water_withdrawal_ds.variables['lat'][:], energy_min_twh[year_index], cmap='Blues', shading='auto')

plt.colorbar(c_min, ax=ax, label='Minimum Energy Use (TWh)')

# Set title and labels
plt.title(f'Minimum Energy Required to Pump Groundwater in the Netherlands (2015)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Display plot
plt.show()

# Now plot the maximum energy use separately
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.plot(ax=ax, color='none', edgecolor='black')

# Plot max energy consumption for 2015
c_max = ax.pcolormesh(water_withdrawal_ds.variables['lon'][:], water_withdrawal_ds.variables['lat'][:], energy_max_twh[year_index], cmap='Reds', shading='auto')

plt.colorbar(c_max, ax=ax, label='Maximum Energy Use (TWh)')

# Set title and labels
plt.title(f'Maximum Energy Required to Pump Groundwater in the Netherlands (2015)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Display plot
plt.show()
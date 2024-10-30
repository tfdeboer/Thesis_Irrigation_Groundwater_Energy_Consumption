import netCDF4 as nc
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import Point

# Constants
g = 9.8  # gravity [m/s^2]
rho = 1000  # density of water [kg/m^3]
eta_min = 0.4  # minimum pump efficiency
eta_max = 0.7  # maximum pump efficiency
conversion_factor = 3.6e6  # to convert J to kWh
dt = 365 * 24 * 3600  # Time in seconds per year

# File paths
groundwater_nc_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/globgm_top_5arcmin_monthly_1958_2015_netherlands.nc'
water_withdrawal_nc_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/irrGWWW_m3_year_1960_2019_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/shp/NL/Netherlands.shp'

# Load the shapefile
gdf = gpd.read_file(shapefile_path)
shapefile_crs = gdf.crs

# Load the groundwater data
groundwater_ds = nc.Dataset(groundwater_nc_path)
groundwater_depth = groundwater_ds.variables['groundwater_depth'][:]
time_groundwater = nc.num2date(groundwater_ds.variables['time'][:], units=groundwater_ds.variables['time'].units)
groundwater_lon = groundwater_ds.variables['lon'][:]
groundwater_lat = groundwater_ds.variables['lat'][:]

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
withdrawal_lon = water_withdrawal_ds.variables['lon'][:]
withdrawal_lat = water_withdrawal_ds.variables['lat'][:]

# Mirror (flip) the withdrawal latitude to see if that aligns better
withdrawal_lat_flipped = withdrawal_lat[::-1]

# Calculate the energy required to pump groundwater per year in MWh
energy_max = np.zeros((len(years), water_withdrawal.shape[1], water_withdrawal.shape[2]))

for i, year in enumerate(years):
    H = annual_groundwater_depth[i]
    Q = np.squeeze(water_withdrawal[i]) / dt  # Convert annual m³/year to m³/s
    
    # Ensure H and Q have the same shape
    if H.shape != Q.shape:
        raise ValueError(f"Shape mismatch: H shape {H.shape}, Q shape {Q.shape}")
    
    # Calculate energy for max efficiency
    energy_max[i] = (g * H * rho * Q) / (conversion_factor * eta_max)  # in MWh

# Select a specific year for visualization
year_index = -20  # Index for 2015, adjust if necessary

# Set up the plot with Cartopy for geographic boundaries
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
gdf.boundary.plot(ax=ax, color='black', linewidth=1)  # Plot the Netherlands shapefile

# Plot the maximum energy consumption for 2015 with flipped latitudes
c_max = ax.pcolormesh(withdrawal_lon, withdrawal_lat_flipped, energy_max[year_index], cmap='Reds', shading='auto')

# Add coastlines and borders for visual reference
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Add a colorbar for maximum energy use
plt.colorbar(c_max, ax=ax, label='Maximum Energy Use (MWh)')

# Set title and labels
plt.title(f'Energy Required to Pump Groundwater in the Netherlands (2015)', fontsize=16, pad=20)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Display plot
plt.tight_layout()
plt.show()
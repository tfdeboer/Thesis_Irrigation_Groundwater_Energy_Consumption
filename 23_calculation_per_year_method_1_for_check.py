import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Constants
g = 9.8  # Gravity [m/s^2]
rho = 1000  # Density of water [kg/m^3]
conversion_factor = 3.6e6  # To convert J to kWh
dt = 365 * 24 * 3600  # Seconds in a year

# Pump efficiency
pump_efficiency = 0.55  # Use 55% efficiency for this visualization

# File paths (vervang door je eigen paden)
groundwater_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/globgm_top_5arcmin_monthly_1958_2015_netherlands.nc'
withdrawal_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/irrGWWW_m3_year_1960_2019_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'


# Load the groundwater data (monthly data)
groundwater_ds = nc.Dataset(groundwater_file)
groundwater_depth = groundwater_ds.variables['groundwater_depth'][:]  # Assuming this is the variable
time_groundwater = nc.num2date(groundwater_ds.variables['time'][:], units=groundwater_ds.variables['time'].units)

# Load the water withdrawal data (yearly data)
withdrawal_ds = nc.Dataset(withdrawal_file)
water_withdrawal = withdrawal_ds.variables['irrigation_withdrawal'][:]  # Assuming this is the variable
time_withdrawal = nc.num2date(withdrawal_ds.variables['time'][:], units=withdrawal_ds.variables['time'].units)

# Extract years and months from the time variables
years_groundwater = np.array([dt.year for dt in time_groundwater])
months_groundwater = np.array([dt.month for dt in time_groundwater])
years_withdrawal = np.array([dt.year for dt in time_withdrawal])

# Select data for the year 2003 and the month of August
target_year = 2003
target_month = 8

# Filter for the specific year and month in groundwater data
year_month_mask_groundwater = (years_groundwater == target_year) & (months_groundwater == target_month)
groundwater_august_2003 = groundwater_depth[year_month_mask_groundwater, :, :, 0].squeeze()  # Select August 2003 data

# Water withdrawal data for the target year
year_index_withdrawal = np.where(years_withdrawal == target_year)[0][0]
Q_2003 = np.squeeze(water_withdrawal[year_index_withdrawal, :, :])  # Water withdrawal for 2003

# Check if shapes match
if groundwater_august_2003.shape != Q_2003.shape:
    raise ValueError(f"Shape mismatch: Groundwater shape {groundwater_august_2003.shape}, Water withdrawal shape {Q_2003.shape}")

# Function to calculate energy consumption for a given depth and withdrawal
def calculate_energy(H, Q, pump_efficiency):
    H = H  # Convert positive values to depth (distance from surface)
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency) * 0.001  # Convert kWh to MWh
    return energy

# Calculate energy consumption for August 2003 per pixel
yearly_energy_per_pixel_2003 = np.zeros_like(groundwater_august_2003)
valid_mask = ~np.isnan(groundwater_august_2003) & (Q_2003 > 0)  # Only compute for valid pixels with positive Q
yearly_energy_per_pixel_2003[valid_mask] = calculate_energy(groundwater_august_2003[valid_mask], Q_2003[valid_mask], pump_efficiency)

# Load the shapefile
shapefile = gpd.read_file(shapefile_path)

# Create a plot with the shapefile and the energy consumption data for August 2003
fig, ax = plt.subplots(figsize=(10, 12), subplot_kw={'projection': ccrs.PlateCarree()})

# Add shapefile boundaries to the plot
shapefile.plot(ax=ax, edgecolor='black', facecolor='none')

# Plot the energy consumption as a heatmap
lon = groundwater_ds.variables['lon'][:]
lat = groundwater_ds.variables['lat'][:]
mesh = ax.pcolormesh(lon, lat, yearly_energy_per_pixel_2003, cmap='viridis', transform=ccrs.PlateCarree(), vmin=0, vmax=0.1)

# Add colorbar
cbar = plt.colorbar(mesh, ax=ax, orientation='horizontal', pad=0.05)
cbar.set_label('Energy Consumption [MWh] (August 2003)', fontsize=16)
cbar.ax.tick_params(labelsize=12)

# Add gridlines and labels
ax.set_title('Groundwater Pump Energy Consumption for Irrigation in August 2003', fontsize=18, pad=20)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Show the plot
plt.tight_layout()
plt.show()
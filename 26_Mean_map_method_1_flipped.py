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

# File paths
groundwater_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/globgm_top_5arcmin_monthly_1958_2015_netherlands.nc'
withdrawal_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/irrGWWW_m3_year_1960_2019_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'

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

# Filter data for the desired period (1980-2015)
year_mask = (years_groundwater >= 1980) & (years_groundwater <= 2015)
groundwater_depth = groundwater_depth[year_mask, :, :, :]
years_groundwater = years_groundwater[year_mask]

# Flip the latitude array of the withdrawal data to match the groundwater data
withdrawal_lat = withdrawal_ds.variables['lat'][:]
withdrawal_lat_flipped = withdrawal_lat[::-1]

# Initialize a variable to store the total energy consumption per pixel over the entire period
total_energy_per_pixel = np.zeros(groundwater_depth.shape[1:3])  # Shape: [lat, lon]

# Function to calculate energy consumption for a given depth and withdrawal
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency) * 0.001  # Convert kWh to MWh
    return energy

# Loop over the years and calculate energy consumption per pixel
for year in range(1980, 2016):  # 1980 to 2015 inclusive
    if year in years_groundwater and year in years_withdrawal:
        # Get groundwater data for the current year
        year_mask_groundwater = years_groundwater == year
        yearly_data = groundwater_depth[year_mask_groundwater, :, :, 0]  # Select all months for the year

        # Calculate mean over all months per pixel for the year
        yearly_mean_per_pixel = np.nanmean(yearly_data, axis=0)  # Mean over months for each pixel

        # Get water withdrawal data for the corresponding year
        year_index_withdrawal = np.where(years_withdrawal == year)[0][0]
        Q = np.squeeze(water_withdrawal[year_index_withdrawal, ::-1, :, 0])  # Flip the water withdrawal data using ::-1 for latitude

        # Ensure the shape matches
        if yearly_mean_per_pixel.shape == Q.shape:
            # Calculate energy per pixel for the year
            yearly_energy_per_pixel = calculate_energy(yearly_mean_per_pixel, Q, pump_efficiency)
            # Add to the total energy per pixel over the entire period
            total_energy_per_pixel += np.nan_to_num(yearly_energy_per_pixel)  # Convert NaNs to 0 for safe addition

# Calculate the average energy consumption per pixel
average_energy_per_pixel = total_energy_per_pixel / len(range(1980, 2016))

# Mask data outside the shapefile boundary
average_energy_per_pixel = np.ma.masked_where(average_energy_per_pixel == 0, average_energy_per_pixel)

# Load the shapefile
shapefile = gpd.read_file(shapefile_path)

# Create a plot with the shapefile and the average energy consumption data
fig, ax = plt.subplots(figsize=(10, 12), subplot_kw={'projection': ccrs.PlateCarree()})

# Add shapefile boundaries to the plot
shapefile.boundary.plot(ax=ax, edgecolor='black')

# Plot the energy consumption as a heatmap
lon = groundwater_ds.variables['lon'][:]
lat = withdrawal_lat_flipped  # Use the flipped latitude for plotting
mesh = ax.pcolormesh(lon, lat, average_energy_per_pixel, cmap='viridis', transform=ccrs.PlateCarree(), vmin=0.0001, vmax=0.1)

# Add colorbar
cbar = plt.colorbar(mesh, ax=ax, orientation='horizontal', pad=0.05)
cbar.set_label('Average Energy Consumption [MWh] (1980-2015)', fontsize=16)
cbar.ax.tick_params(labelsize=12)

# Add gridlines and labels
ax.set_title('Average Groundwater Pump Energy Consumption for Irrigation (1980-2015)', fontsize=18, pad=20)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Display plot
plt.tight_layout()
plt.show()
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

# Extract years from the time variables
years_groundwater = np.array([dt.year for dt in time_groundwater])
years_withdrawal = np.array([dt.year for dt in time_withdrawal])

# Filter data for the desired period (1980-2015)
year_mask = (years_groundwater >= 1980) & (years_groundwater <= 2015)
groundwater_depth = groundwater_depth[year_mask, :, :, :]
years_groundwater = years_groundwater[year_mask]

# Function to calculate energy consumption for a given depth and withdrawal
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency) * 0.001  # Convert kWh to MWh
    return energy

# Load the shapefile
shapefile = gpd.read_file(shapefile_path)

# Get the longitude and latitude coordinates
lon = groundwater_ds.variables['lon'][:]
lat = groundwater_ds.variables['lat'][:]

# Loop over each year (1980-2015) and create a plot for each year
for year in range(1980, 2016):  # 1980 to 2015 inclusive
    if year in years_groundwater and year in years_withdrawal:
        # Get groundwater data for the current year
        year_mask_groundwater = years_groundwater == year
        yearly_data = groundwater_depth[year_mask_groundwater, :, :, 0]  # Select all months for the year

        # Calculate mean over all months per pixel for the year
        yearly_mean_per_pixel = np.nanmean(yearly_data, axis=0)  # Mean over months for each pixel

        # Get water withdrawal data for the corresponding year
        year_index_withdrawal = np.where(years_withdrawal == year)[0][0]
        Q = np.squeeze(water_withdrawal[year_index_withdrawal, :, :, 0])  # Water withdrawal for the year

        # Ensure the shape matches
        if yearly_mean_per_pixel.shape == Q.shape:
            # Calculate energy per pixel for the year
            yearly_energy_per_pixel = calculate_energy(yearly_mean_per_pixel, Q, pump_efficiency)

            # Create a plot with the shapefile and the energy consumption data for the current year
            fig, ax = plt.subplots(figsize=(10, 12), subplot_kw={'projection': ccrs.PlateCarree()})
            
            # Add shapefile boundaries to the plot
            shapefile.plot(ax=ax, edgecolor='black', facecolor='none')

            # Plot the energy consumption as a heatmap
            mesh = ax.pcolormesh(lon, lat, yearly_energy_per_pixel, cmap='viridis', transform=ccrs.PlateCarree(), vmin=0, vmax=1)

            # Add colorbar
            cbar = plt.colorbar(mesh, ax=ax, orientation='horizontal', pad=0.05)
            cbar.set_label(f'Energy Consumption [MWh] in {year}', fontsize=16)
            cbar.ax.tick_params(labelsize=12)

            # Add gridlines and labels
            ax.set_title(f'Groundwater Pump Energy Consumption for Irrigation ({year})', fontsize=18, pad=20)
            ax.add_feature(cfeature.COASTLINE)
            ax.add_feature(cfeature.BORDERS, linestyle=':')

            # Show the plot
            plt.tight_layout()
            plt.show()
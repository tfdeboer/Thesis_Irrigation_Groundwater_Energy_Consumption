import netCDF4 as nc
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.8  # gravity [m/s^2]
rho = 1000  # density of water [kg/m^3]
conversion_factor = 3.6e6  # to convert J to kWh

# Adjustable pump efficiency (change this value to adjust efficiency)
pump_efficiency = 0.7  # Set the pump efficiency here (0.0 - 1.0)

# Toggle for including the radius of influence in the lift height calculation
use_radius_of_influence = False  # Set to True if you want to include the radius of influence

# Define parameters for radius of influence formula (currently placeholders)
rw = 0.1  # radius of the pumped well [m], placeholder value
R = 100  # radius of influence [m], placeholder value
K = 10  # hydraulic conductivity [m/day], placeholder value
D = 50  # aquifer depth [m], placeholder value

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

# Calculate annual average groundwater depth (hr) from monthly data
years = np.arange(1980, 2016)
annual_groundwater_depth = np.zeros((len(years), groundwater_depth.shape[1], groundwater_depth.shape[2]))

for i, year in enumerate(years):
    mask = np.array([dt.year == year for dt in time_groundwater])
    yearly_data = np.mean(groundwater_depth[mask], axis=0)
    yearly_data = np.squeeze(yearly_data)
    annual_groundwater_depth[i] = yearly_data

# Load the water withdrawal data
water_withdrawal_ds = nc.Dataset(water_withdrawal_nc_path)
water_withdrawal = water_withdrawal_ds.variables['irrigation_withdrawal'][:]
time_water_withdrawal = nc.num2date(water_withdrawal_ds.variables['time'][:], units=water_withdrawal_ds.variables['time'].units)

# Calculate the energy required to pump groundwater per year
energy = np.zeros((len(years), water_withdrawal.shape[1], water_withdrawal.shape[2]))

for i, year in enumerate(years):
    hr = annual_groundwater_depth[i]
    Q = np.squeeze(water_withdrawal[i])
    dt = 365 * 24 * 3600  # Time in seconds per year
    
    # Calculate the total lift height H
    if use_radius_of_influence:
        # Calculate the contribution from the radius of influence
        radius_contribution = (Q / (2 * np.pi * K * D)) * np.log(rw / R)
        
        # Adjust H accordingly: 
        # - Subtract the radius contribution to correctly reflect the deeper groundwater level.
        H = hr - radius_contribution
    else:
        H = hr
    
    # Ensure H and Q have the same shape
    if H.shape != Q.shape:
        raise ValueError(f"Shape mismatch: H shape {H.shape}, Q shape {Q.shape}")
    
    energy[i] = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency)

# Convert energy to TWh for easier interpretation
energy_twh = energy / 1e9

# Function to calculate and plot energy consumption
def plot_energy_consumption(start_year=None, end_year=None, lat_lon=None):
    if start_year is None or end_year is None:
        selected_energy = np.mean(energy_twh, axis=0)  # Average over the entire range
        title_year = '1980-2015 (Average)'
        total_energy_avg = np.mean(np.sum(energy_twh, axis=(1, 2)))
        print(f"Average annual energy consumption for the Netherlands over 1980-2015: {total_energy_avg:.2f} TWh")
    elif start_year == end_year:
        year_index = list(years).index(start_year)
        selected_energy = energy_twh[year_index]
        title_year = str(start_year)
        total_energy_year = np.sum(selected_energy)
        print(f"Total energy consumption for the Netherlands in {start_year}: {total_energy_year:.2f} TWh")
    else:
        start_idx = list(years).index(start_year)
        end_idx = list(years).index(end_year)
        selected_energy = np.mean(energy_twh[start_idx:end_idx+1], axis=0)
        title_year = f'{start_year}-{end_year} (Average)'
        total_energy_avg = np.mean(np.sum(energy_twh[start_idx:end_idx+1], axis=(1, 2)))
        print(f"Average annual energy consumption for the Netherlands over {start_year}-{end_year}: {total_energy_avg:.2f} TWh")

    # Proceed with plotting as usual
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    c = ax.pcolormesh(water_withdrawal_ds.variables['lon'][:], water_withdrawal_ds.variables['lat'][:], selected_energy, cmap='Blues', shading='auto')
    gdf.boundary.plot(ax=ax, linewidth=1, edgecolor='black')
    cbar = plt.colorbar(c, ax=ax, label=f'Energy Use [TWh] with {pump_efficiency * 100:.0f}% Pump Efficiency')
    cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
    plt.title(f'Energy Required to Pump Groundwater in the Netherlands ({title_year})')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    # If lat_lon is provided, display the specific pixel value
    if lat_lon:
        lat_val, lon_val = lat_lon
        lat_idx = np.abs(water_withdrawal_ds.variables['lat'][:] - lat_val).argmin()
        lon_idx = np.abs(water_withdrawal_ds.variables['lon'][:] - lon_val).argmin()
        pixel_value = selected_energy[lat_idx, lon_idx]
        print(f'Energy use at ({lat_val}, {lon_val}) during {title_year}: {pixel_value:.2f} TWh')

# Example usage:
# To visualize a specific year, e.g., 2015
plot_energy_consumption(start_year=2000, end_year=2000, lat_lon=(51.55, 4.7))

# To visualize the average energy consumption over a range of years, e.g., 1990-2000
# plot_energy_consumption(start_year=1990, end_year=2000, lat_lon=(52.1, 5.2))

# To visualize the average energy consumption over the entire range (1980-2015)
# plot_energy_consumption(lat_lon=(52.1, 5.2))

import netCDF4 as nc
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Constants
g = 9.8  # gravity [m/s^2]
rho = 1000  # density of water [kg/m^3]
conversion_factor = 3.6e6  # to convert J to kWh

# Toggle for including the radius of influence in the lift height calculation
use_radius_of_influence = False  # Set to True if you want to include the radius of influence

# Define parameters for radius of influence formula (currently placeholders)
rw = 0.1  # radius of the pumped well [m], placeholder value
R = 100  # radius of influence [m], placeholder value
K = 10  # hydraulic conductivity [m/day], placeholder value
D = 50  # aquifer depth [m], placeholder value

# Bias correction value
bias_correction = 0.4539  # Bias correction value to be subtracted from model data

# File paths
groundwater_nc_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/globgm_top_5arcmin_monthly_1958_2015_netherlands.nc'
water_withdrawal_nc_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/irrGWWW_m3_year_1960_2019_NL.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/shp/NL/Netherlands.shp'
electricity_consumption_csv = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/nc/eia_electricity_net_consumption_TWh_NL.csv'

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
    
    # Apply bias correction
    yearly_data_corrected = yearly_data - bias_correction
    
    annual_groundwater_depth[i] = yearly_data_corrected

# Load the water withdrawal data
water_withdrawal_ds = nc.Dataset(water_withdrawal_nc_path)
water_withdrawal = water_withdrawal_ds.variables['irrigation_withdrawal'][:]
time_water_withdrawal = nc.num2date(water_withdrawal_ds.variables['time'][:], units=water_withdrawal_ds.variables['time'].units)

# Function to calculate energy consumption for a given pump efficiency
def calculate_energy_consumption(pump_efficiency):
    energy = np.zeros((len(years), water_withdrawal.shape[1], water_withdrawal.shape[2]))

    for i, year in enumerate(years):
        hr = annual_groundwater_depth[i]
        Q = np.squeeze(water_withdrawal[i])
        dt = 365 * 24 * 3600  # Time in seconds per year

        # Calculate the total lift height H
        if use_radius_of_influence:
            # Calculate the contribution from the radius of influence
            radius_contribution = (Q / (2 * np.pi * K * D)) * np.log(rw / R)
            # Adjust H accordingly
            H = hr - radius_contribution
        else:
            H = hr

        # Ensure H and Q have the same shape
        if H.shape != Q.shape:
            raise ValueError(f"Shape mismatch: H shape {H.shape}, Q shape {Q.shape}")

        energy[i] = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency)

    # Convert energy to TWh for easier interpretation
    energy_twh = np.sum(energy, axis=(1, 2)) / 1e9  # Total energy consumption per year
    return energy_twh

# Calculate energy consumption for different pump efficiencies
efficiencies = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
energy_results = {}

for eff in efficiencies:
    energy_results[eff] = calculate_energy_consumption(eff)

# Load the electricity net consumption data
electricity_data = pd.read_csv(electricity_consumption_csv)
electricity_years = electricity_data['Year']
electricity_consumption = electricity_data['Total electricity (TWh)']

# Plotting the results
plt.figure(figsize=(12, 8))

for eff, energy in energy_results.items():
    plt.plot(years, energy, label=f'Pump Efficiency = {eff}', marker='o')

# Plot the electricity net consumption for comparison
plt.plot(electricity_years, electricity_consumption, label='Electricity Net Consumption', marker='x', color='black', linestyle='--')

# Customize the plot
plt.xlabel('Year')
plt.ylabel('Energy Consumption (TWh)')
plt.title('Annual Energy Consumption for Water Pumping in Agriculture (1980-2015)')
plt.legend()
plt.grid(True)

# Set y-axis limit
plt.ylim(0, 200)  # Set the y-axis scale to have a maximum of 200

plt.show()
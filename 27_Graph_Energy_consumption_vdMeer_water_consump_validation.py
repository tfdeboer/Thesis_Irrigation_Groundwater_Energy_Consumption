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

# File paths
groundwater_csv_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/tables/Observed_data/Mean_stdv_groundwater_heads_per_year.csv'
electricity_consumption_csv = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/nc/eia_electricity_net_consumption_TWh_NL.csv'
waterwithdrawal_csv = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/tables/Observed_data/Validation_data_grondwater_irrigatie_vdMeer_2001_2021.csv'

# Load the observed water withdrawal data
waterwithdrawal_data = pd.read_csv(waterwithdrawal_csv)
waterwithdrawal_data['Grondwater (irrigatie)'] = waterwithdrawal_data['Grondwater (irrigatie)'] * 1e6  # Convert to cubic meters
withdrawal_years = waterwithdrawal_data['Year']
water_withdrawal = waterwithdrawal_data['Grondwater (irrigatie)'].values

# Load the observed average groundwater data from CSV
groundwater_data = pd.read_csv(groundwater_csv_path)
groundwater_years = groundwater_data['Year']
groundwater_depth = groundwater_data['Mean_Groundwater']  # Depth in meters (positive means deeper)

# Filter for overlapping years (2001-2015)
overlap_mask = (groundwater_years >= 2001) & (groundwater_years <= 2015)
groundwater_years_filtered = groundwater_years[overlap_mask].reset_index(drop=True)  # Reset index
groundwater_depth_filtered = groundwater_depth[overlap_mask].reset_index(drop=True)  # Reset index

# Ensure that the withdrawal and groundwater datasets align for the overlapping period
withdrawal_years_filtered = withdrawal_years[withdrawal_years <= 2015].reset_index(drop=True)  # Reset index
water_withdrawal_filtered = water_withdrawal[:len(withdrawal_years_filtered)]

if not np.array_equal(groundwater_years_filtered, withdrawal_years_filtered):
    raise ValueError("Years in the filtered groundwater and water withdrawal datasets do not match!")

# Function to calculate energy consumption for a given pump efficiency
def calculate_energy_consumption(pump_efficiency):
    energy = np.zeros(len(groundwater_years_filtered))

    for i, year in enumerate(groundwater_years_filtered):
        hr = groundwater_depth_filtered[i]  # Average groundwater depth for the year
        Q = water_withdrawal_filtered[i]/(24*3600)  # Water withdrawal from CSV data (in cubic meters)
        dt = 365 * 24 * 3600  # Time in seconds per year

        # Calculate the total lift height H
        if use_radius_of_influence:
            radius_contribution = (Q / (2 * np.pi * K * D)) * np.log(rw / R)
            H = hr - radius_contribution
        else:
            H = hr

        # Ensure H is positive (since a positive depth is deeper)
        H = abs(H)

        # Calculate energy (Joules) and convert to TWh
        energy[i] = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency)

    return energy / 1e9  # Convert to TWh

# Calculate energy consumption for different pump efficiencies
efficiency_low = 0.4
efficiency_high = 0.7
energy_low = calculate_energy_consumption(efficiency_low)
energy_high = calculate_energy_consumption(efficiency_high)

# Check if there is variation in energy calculations
print(f"Energy consumption (low efficiency 0.4): {energy_low}")
print(f"Energy consumption (high efficiency 0.7): {energy_high}")

# Load the electricity net consumption data
electricity_data = pd.read_csv(electricity_consumption_csv)
electricity_years = electricity_data['Year']
electricity_consumption = electricity_data['Total electricity (TWh)']

# Plotting the results
plt.figure(figsize=(12, 8))

# Plot the energy consumption for pump efficiencies 0.4 and 0.7
plt.plot(groundwater_years_filtered, energy_low, label=f'Pump Efficiency = {efficiency_low}', color='#1f77b4', linestyle='--')
plt.plot(groundwater_years_filtered, energy_high, label=f'Pump Efficiency = {efficiency_high}', color='#ff7f0e', linestyle='--')

# Fill the area between pump efficiency 0.4 and 0.7
plt.fill_between(groundwater_years_filtered, energy_low, energy_high, color='gray', alpha=0.3, label='Range of Pump Efficiency (0.4 - 0.7)')

# Plot the electricity net consumption for comparison
plt.plot(electricity_years, electricity_consumption, label='Electricity Net Consumption', marker='x', color='black', linestyle='-', linewidth=2)

# Customize the plot
plt.xlabel('Year')
plt.ylabel('Energy Consumption (TWh)')
plt.title('Annual Energy Consumption for Water Pumping in Agriculture (2001-2015)')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(2000, 2016)
plt.ylim(0, 10)

plt.tight_layout()
plt.show()
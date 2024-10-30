import netCDF4 as nc
import numpy as np
import pandas as pd

# Constants
g = 9.8  # gravity [m/s^2]
rho = 1000  # density of water [kg/m^3]
conversion_factor = 3.6e6  # to convert J to kWh
dt = 365 * 24 * 3600  # seconds in a year

# Pump efficiencies for different scenarios
pump_efficiency_40 = 0.4  # 40% pump efficiency
pump_efficiency_55 = 0.55  # 55% pump efficiency
pump_efficiency_70 = 0.7  # 70% pump efficiency

# File paths
groundwater_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/globgm_top_5arcmin_monthly_1958_2015_netherlands.nc'
withdrawal_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/Validation_data_grondwater_million_cubic_m3_irrigatie_vdMeer_2001_2021.xlsx'
output_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/groundwater_energie_consumptions_method_3_2001_2015.csv'

# Load the groundwater data (monthly data)
groundwater_ds = nc.Dataset(groundwater_file)
groundwater_depth = groundwater_ds.variables['groundwater_depth'][:]  # Assuming this is the variable
time_groundwater = nc.num2date(groundwater_ds.variables['time'][:], units=groundwater_ds.variables['time'].units)

# Extract years from the groundwater time variable
years_groundwater = np.array([dt.year for dt in time_groundwater])

# Load the observed water withdrawal data from Excel (2001-2021)
df_withdrawal = pd.read_excel(withdrawal_file, sheet_name='Validation_data_grondwater_irri')
years_observed = df_withdrawal['Year']
total_withdrawal_per_year = df_withdrawal['Grondwater_irrigatie_m^3'] * 1e6  # Convert million m³ to m³

# Initialize lists to store results
yearly_mean = []
energy_efficiency_40 = []
energy_efficiency_55 = []
energy_efficiency_70 = []

# Function to calculate energy consumption in MWh
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency)  # Convert to kWh
    energy_mwh = energy / 1e3  # Convert kWh to MWh
    return energy_mwh

# Loop over the years 2001-2021 and calculate energy consumption
for year in range(2001, 2022):
    # Default values to NaN
    avg_groundwater_depth = np.nan
    energy_40 = np.nan
    energy_55 = np.nan
    energy_70 = np.nan

    # Get groundwater data for the current year
    if year in years_groundwater:
        year_mask_groundwater = years_groundwater == year
        yearly_data = groundwater_depth[year_mask_groundwater, :, :, 0]  # Select all months for the year, ignore unnecessary dimension

        # Calculate mean over all months per pixel for the year
        yearly_mean_per_pixel = np.nanmean(yearly_data, axis=0)  # Mean over months for each pixel

        # Calculate the overall mean for the entire year
        avg_groundwater_depth = np.nanmean(yearly_mean_per_pixel)  # Average over all pixels

        # Get water withdrawal for the corresponding year from observed data
        if year in years_observed.values:
            total_Q = total_withdrawal_per_year[years_observed == year].values[0]  # Total water withdrawal in m³

            # Calculate energy for 40%, 55%, and 70% pump efficiency
            energy_40 = calculate_energy(avg_groundwater_depth, total_Q, pump_efficiency_40)
            energy_55 = calculate_energy(avg_groundwater_depth, total_Q, pump_efficiency_55)
            energy_70 = calculate_energy(avg_groundwater_depth, total_Q, pump_efficiency_70)

    # Store results for each year
    yearly_mean.append(avg_groundwater_depth)
    energy_efficiency_40.append(energy_40)
    energy_efficiency_55.append(energy_55)
    energy_efficiency_70.append(energy_70)

# Create a DataFrame to store the results
df_results = pd.DataFrame({
    'Year': years_observed,
    'Mean_Groundwater_Depth_m': yearly_mean,
    'Total_Withdrawal_m3': total_withdrawal_per_year,
    'Pump_Efficiency_40%_MWh': energy_efficiency_40,
    'Pump_Efficiency_55%_MWh': energy_efficiency_55,
    'Pump_Efficiency_70%_MWh': energy_efficiency_70
})

# Save the results to a CSV file
df_results.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")
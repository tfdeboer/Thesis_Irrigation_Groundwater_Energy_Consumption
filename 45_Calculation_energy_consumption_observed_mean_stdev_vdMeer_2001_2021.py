import netCDF4 as nc
import numpy as np
import pandas as pd

# Constants
g = 9.8  # gravity [m/s^2]
rho = 1000  # density of water [kg/m^3]
conversion_factor = 3.6e6  # to convert J to kWh
dt = 365 * 24 * 3600  # seconds in a year
pump_efficiency_low = 0.4  # lower pump efficiency
pump_efficiency_high = 0.7  # higher pump efficiency

# File paths
groundwater_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/globgm_top_5arcmin_monthly_1958_2015_netherlands.nc'
withdrawal_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/Validation_data_grondwater_million_cubic_m3_irrigatie_vdMeer_2001_2021.xlsx'
output_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/observed_groundwater_energy_consumption_with_correcte_mean_stddev_2001_2021_script_45.csv'

# Load the groundwater data (monthly data)
groundwater_ds = nc.Dataset(groundwater_file)
groundwater_depth = groundwater_ds.variables['groundwater_depth'][:]  # Assuming this is the variable
time_groundwater = nc.num2date(groundwater_ds.variables['time'][:], units=groundwater_ds.variables['time'].units)

# Extract years from the groundwater time variable
years_groundwater = np.array([dt.year for dt in time_groundwater])

# Load the observed water withdrawal data from Excel (2001-2021)
df_withdrawal = pd.read_excel(withdrawal_file, sheet_name='Validation_data_grondwater_irri')
years_observed = df_withdrawal['Year']
total_withdrawal_per_year = df_withdrawal['Grondwater_irrigatie_m^3']   # is already in millions m³

# Initialize lists to store results
yearly_mean = []
yearly_stddev = []
energy_low_efficiency = []
energy_high_efficiency = []
energy_low_upper = []
energy_low_lower = []
energy_high_upper = []
energy_high_lower = []

# Function to calculate energy consumption
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = ((g * H * rho * Q * dt) / (conversion_factor * pump_efficiency)) * 1e-9  # Convert to TWh
    return energy

# Loop over the years 2001-2021 and calculate energy consumption
for year in range(2001, 2022):
    # Default values to NaN
    avg_groundwater_depth = np.nan
    avg_stddev_groundwater_depth = np.nan
    energy_low = np.nan
    energy_high = np.nan
    energy_low_up = np.nan
    energy_low_low = np.nan
    energy_high_up = np.nan
    energy_high_low = np.nan

    # Get groundwater data for the current year
    if year in years_groundwater:
        year_mask_groundwater = years_groundwater == year
        yearly_data = groundwater_depth[year_mask_groundwater, :, :, 0]  # Select all months for the year, ignore unnecessary dimension

        # Calculate mean and stddev over all months per pixel for the year
        yearly_mean_per_pixel = np.nanmean(yearly_data, axis=0)  # Mean over months for each pixel
        yearly_stddev_per_pixel = np.nanstd(yearly_data, axis=0)  # Stddev over months for each pixel

        # Calculate the overall mean and stddev for the entire year
        avg_groundwater_depth = np.nanmean(yearly_mean_per_pixel)  # Average over all pixels
        avg_stddev_groundwater_depth = np.nanmean(yearly_stddev_per_pixel)  # Average stddev over all pixels

        # Get water withdrawal for the corresponding year from observed data
        if year in years_observed.values:
            total_Q = total_withdrawal_per_year[years_observed == year].values[0]  # Total water withdrawal in m³

            # Calculate energy for both low and high pump efficiency
            energy_low = calculate_energy(avg_groundwater_depth, total_Q, pump_efficiency_low)
            energy_high = calculate_energy(avg_groundwater_depth, total_Q, pump_efficiency_high)

            # Calculate energy for H ± stddev(H) for uncertainty
            energy_low_up = calculate_energy(avg_groundwater_depth + avg_stddev_groundwater_depth, total_Q, pump_efficiency_low)
            energy_low_low = calculate_energy(avg_groundwater_depth - avg_stddev_groundwater_depth, total_Q, pump_efficiency_low)

            energy_high_up = calculate_energy(avg_groundwater_depth + avg_stddev_groundwater_depth, total_Q, pump_efficiency_high)
            energy_high_low = calculate_energy(avg_groundwater_depth - avg_stddev_groundwater_depth, total_Q, pump_efficiency_high)

    # Store results for each year
    yearly_mean.append(avg_groundwater_depth)
    yearly_stddev.append(avg_stddev_groundwater_depth)
    energy_low_efficiency.append(energy_low)
    energy_high_efficiency.append(energy_high)
    energy_low_upper.append(energy_low_up)
    energy_low_lower.append(energy_low_low)
    energy_high_upper.append(energy_high_up)
    energy_high_lower.append(energy_high_low)

# Create a DataFrame to store the results
df_results = pd.DataFrame({
    'Year': years_observed,
    'Mean_Groundwater_Depth_m': yearly_mean,
    'StdDev_Groundwater_Depth_m': yearly_stddev,
    'Total_Withdrawal_m3': total_withdrawal_per_year,
    'Energy_Low_Efficiency_TWh': energy_low_efficiency,
    'Energy_High_Efficiency_TWh': energy_high_efficiency,
    'Energy_Low_Efficiency_Upper_TWh': energy_low_upper,
    'Energy_Low_Efficiency_Lower_TWh': energy_low_lower,
    'Energy_High_Efficiency_Upper_TWh': energy_high_upper,
    'Energy_High_Efficiency_Lower_TWh': energy_high_lower
})

# Save the results to a CSV file
df_results.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")
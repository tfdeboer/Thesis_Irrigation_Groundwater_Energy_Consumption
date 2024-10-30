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
pump_efficiency_55 = 0.55  # 55% pump efficiency (new efficiency level)
pump_efficiency_70 = 0.7  # 70% pump efficiency

# File paths
groundwater_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/globgm_top_5arcmin_monthly_1958_2015_netherlands.nc'
withdrawal_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/irrGWWW_m3_year_1960_2019_NL.nc'
output_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/groundwater_energy_consumption_method_1.csv'

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

# Get the unique years for both datasets
unique_years_groundwater = np.unique(years_groundwater)
unique_years_withdrawal = np.unique(years_withdrawal)

# Initialize lists to store results
yearly_mean = []
total_withdrawal_per_year = []
energy_efficiency_40 = []
energy_efficiency_55 = []
energy_efficiency_70 = []

# Function to calculate energy consumption
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency) * 1e-3  # Convert to MWh
    return energy

# Loop over the years (1960–2019, considering the overlap of both datasets)
for year in range(1960, 2020):
    if year in unique_years_groundwater and year in unique_years_withdrawal:
        # Get groundwater data for the current year
        year_mask_groundwater = years_groundwater == year
        yearly_data = groundwater_depth[year_mask_groundwater, :, :, 0]  # Select all months for the year, ignore unnecessary dimension

        # Calculate mean over all months per pixel for the year
        yearly_mean_per_pixel = np.nanmean(yearly_data, axis=0)  # Mean over months for each pixel

        # Calculate the overall mean for the entire year
        avg_groundwater_depth = np.nanmean(yearly_mean_per_pixel)  # Average over all pixels

        # Get water withdrawal data for the corresponding year
        year_index_withdrawal = np.where(years_withdrawal == year)[0][0]
        Q = np.squeeze(water_withdrawal[year_index_withdrawal, :, :, 0])  # Water withdrawal for the year

        # Ensure the shape matches
        if yearly_mean_per_pixel.shape != Q.shape:
            raise ValueError(f"Shape mismatch: Groundwater shape {yearly_mean_per_pixel.shape}, Water withdrawal shape {Q.shape}")
        
        # Calculate total water withdrawal (sum over all pixels)
        total_withdrawal = np.nansum(Q)

        # Calculate energy for 40%, 55%, and 70% pump efficiency
        energy_40 = np.nansum(calculate_energy(yearly_mean_per_pixel, Q, pump_efficiency_40))
        energy_55 = np.nansum(calculate_energy(yearly_mean_per_pixel, Q, pump_efficiency_55))
        energy_70 = np.nansum(calculate_energy(yearly_mean_per_pixel, Q, pump_efficiency_70))

    else:
        # If data is missing for the current year, leave the fields empty
        avg_groundwater_depth = np.nan
        total_withdrawal = np.nan
        energy_40 = np.nan
        energy_55 = np.nan
        energy_70 = np.nan

    # Store the results for each year
    yearly_mean.append(avg_groundwater_depth)
    total_withdrawal_per_year.append(total_withdrawal)
    energy_efficiency_40.append(energy_40)
    energy_efficiency_55.append(energy_55)
    energy_efficiency_70.append(energy_70)

# Create a DataFrame with the new columns
df = pd.DataFrame({
    'Year': range(1960, 2020),
    'Mean_Groundwater_Depth_m': yearly_mean,
    'Total_Withdrawal_m3': total_withdrawal_per_year,
    'Pump_Efficiency_40%_MWh': energy_efficiency_40,
    'Pump_Efficiency_55%_MWh': energy_efficiency_55,
    'Pump_Efficiency_70%_MWh': energy_efficiency_70
})

# Save the DataFrame to a CSV file
df.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")
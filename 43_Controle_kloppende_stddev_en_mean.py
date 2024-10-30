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
withdrawal_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/irrGWWW_m3_year_1960_2019_NL.nc'
output_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/groundwater_energy_consumption_with_correcte_mean_stddev_berekening_per_pixel_script43.csv'

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
yearly_stddev = []
energy_low_efficiency = []
energy_high_efficiency = []
energy_low_upper = []
energy_low_lower = []
energy_high_upper = []
energy_high_lower = []
total_withdrawal_per_year = []

# Function to calculate energy consumption
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency) * 1e-9  # Convert to TWh
    return energy

# Loop over the years (1960–2019, considering the overlap of both datasets)
for year in range(1960, 2020):
    if year in unique_years_groundwater and year in unique_years_withdrawal:
        # Get groundwater data for the current year
        year_mask_groundwater = years_groundwater == year
        yearly_data = groundwater_depth[year_mask_groundwater, :, :, 0]  # Select all months for the year, ignore unnecessary dimension

        # Calculate mean and stddev over all months per pixel for the year
        yearly_mean_per_pixel = np.nanmean(yearly_data, axis=0)  # Mean over months for each pixel
        yearly_stddev_per_pixel = np.nanstd(yearly_data, axis=0)  # Stddev over months for each pixel

        # Calculate the overall mean and stddev for the entire year
        avg_groundwater_depth = np.nanmean(yearly_mean_per_pixel)  # Average over all pixels
        avg_stddev_groundwater_depth = np.nanmean(yearly_stddev_per_pixel)  # Average stddev over all pixels

        # Get water withdrawal data for the corresponding year
        year_index_withdrawal = np.where(years_withdrawal == year)[0][0]
        Q = np.squeeze(water_withdrawal[year_index_withdrawal, :, :, 0])  # Water withdrawal for the year

        # Ensure the shape matches
        if yearly_mean_per_pixel.shape != Q.shape:
            raise ValueError(f"Shape mismatch: Groundwater shape {yearly_mean_per_pixel.shape}, Water withdrawal shape {Q.shape}")
        
        # Calculate total water withdrawal (sum over all pixels)
        total_withdrawal = np.nansum(Q)

        # OPTION 1: Calculate energy per pixel for both low and high pump efficiency
        total_energy_low = np.nansum(calculate_energy(yearly_mean_per_pixel, Q, pump_efficiency_low))
        total_energy_high = np.nansum(calculate_energy(yearly_mean_per_pixel, Q, pump_efficiency_high))

        # OPTION 2: Calculate energy based on overall average depth
        #avg_H = np.nanmean(yearly_mean_per_pixel)  # gemiddelde grondwaterstand voor heel Nederland
        #total_Q = np.nansum(Q)  # totale opgepompte waterhoeveelheid in m³
        #total_energy_low = calculate_energy(avg_H, total_Q, pump_efficiency_low)
        #total_energy_high = calculate_energy(avg_H, total_Q, pump_efficiency_high)

        # NEW: Calculate energy based on H ± stddev(H) for uncertainty
        energy_low_upper.append(calculate_energy(avg_groundwater_depth + avg_stddev_groundwater_depth, total_withdrawal, pump_efficiency_low))
        energy_low_lower.append(calculate_energy(avg_groundwater_depth - avg_stddev_groundwater_depth, total_withdrawal, pump_efficiency_low))

        energy_high_upper.append(calculate_energy(avg_groundwater_depth + avg_stddev_groundwater_depth, total_withdrawal, pump_efficiency_high))
        energy_high_lower.append(calculate_energy(avg_groundwater_depth - avg_stddev_groundwater_depth, total_withdrawal, pump_efficiency_high))
    else:
        # If data is missing for the current year, leave the fields empty
        avg_groundwater_depth = np.nan
        avg_stddev_groundwater_depth = np.nan
        total_withdrawal = np.nan
        total_energy_low = np.nan
        total_energy_high = np.nan

        energy_low_upper.append(np.nan)
        energy_low_lower.append(np.nan)
        energy_high_upper.append(np.nan)
        energy_high_lower.append(np.nan)

    # Store the results for each year
    yearly_mean.append(avg_groundwater_depth)
    yearly_stddev.append(avg_stddev_groundwater_depth)
    total_withdrawal_per_year.append(total_withdrawal)
    energy_low_efficiency.append(total_energy_low)
    energy_high_efficiency.append(total_energy_high)

# Save the results to a CSV file
df = pd.DataFrame({
    'Year': range(1960, 2020),
    'Mean_Groundwater_Depth_m': yearly_mean,
    'StdDev_Groundwater_Depth_m': yearly_stddev,
    'Total_Withdrawal_m3': total_withdrawal_per_year,
    'Energy_Low_Efficiency_TWh_Calc_per_Pixel': energy_low_efficiency,
    'Energy_High_Efficiency_TWh_Calc_per_Pixel': energy_high_efficiency,
    'Energy_Low_Efficiency_Upper_TWh_Calc_per_Pixel': energy_low_upper,
    'Energy_Low_Efficiency_Lower_TWh_Calc_per_Pixel': energy_low_lower,
    'Energy_High_Efficiency_Upper_TWh_Calc_per_Pixel': energy_high_upper,
    'Energy_High_Efficiency_Lower_TWh_Calc_per_Pixel': energy_high_lower
})
df.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")
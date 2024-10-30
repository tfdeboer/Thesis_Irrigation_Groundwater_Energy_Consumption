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
output_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/groundwater_energy_consumption_with_stddev.csv'

# Load the groundwater data (monthly data)
groundwater_ds = nc.Dataset(groundwater_file)
groundwater_depth = groundwater_ds.variables['groundwater_depth'][:]  # Assuming this is the variable
time_groundwater = nc.num2date(groundwater_ds.variables['time'][:], units=groundwater_ds.variables['time'].units)

# Load the water withdrawal data (yearly data)
withdrawal_ds = nc.Dataset(withdrawal_file)
water_withdrawal = withdrawal_ds.variables['irrigation_withdrawal'][:]  # Assuming this is the variable
time_withdrawal = nc.num2date(withdrawal_ds.variables['time'][:], units=withdrawal_ds.variables['time'].units)

# Convert monthly groundwater data to yearly averages (since Q is yearly)
years = np.arange(1960, 2016)  # Common years for groundwater and water withdrawal data
annual_groundwater_depth = []

for year in years:
    mask = np.array([dt.year == year for dt in time_groundwater])
    yearly_mean = np.mean(groundwater_depth[mask, :, :, 0], axis=0)  # Averaging monthly data per year
    annual_groundwater_depth.append(yearly_mean)

annual_groundwater_depth = np.array(annual_groundwater_depth)  # Convert list to array

# Function to calculate energy consumption
def calculate_energy(H, Q, pump_efficiency):
    Q = Q / dt  # Convert m³/year to m³/s
    energy = (g * H * rho * Q * dt) / (conversion_factor * pump_efficiency) * 1e-9  # Convert to TWh
    return energy

# Store results
results = []

for i, year in enumerate(years):
    H = annual_groundwater_depth[i]  # Groundwater depth for the year
    Q = np.squeeze(water_withdrawal[i, :, :, 0])  # Water withdrawal for the year
    
    # Ensure shapes match
    if H.shape != Q.shape:
        raise ValueError(f"Shape mismatch: H shape {H.shape}, Q shape {Q.shape}")
    
    # Calculate total energy for both low and high pump efficiency
    energy_low = np.nansum(calculate_energy(H, Q, pump_efficiency_low))
    energy_high = np.nansum(calculate_energy(H, Q, pump_efficiency_high))
    
    # Calculate average groundwater depth and standard deviation for the year
    avg_groundwater_depth = np.nanmean(H)
    stddev_groundwater_depth = np.nanstd(H)
    
    # Save results for the year
    results.append({
        'Year': year,
        'Avg_Groundwater_Depth_m': avg_groundwater_depth,
        'StdDev_Groundwater_Depth_m': stddev_groundwater_depth,
        'Energy_Low_Efficiency_TWh': energy_low,
        'Energy_High_Efficiency_TWh': energy_high
    })

# Convert results to DataFrame and save to CSV
df_results = pd.DataFrame(results)
df_results.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")
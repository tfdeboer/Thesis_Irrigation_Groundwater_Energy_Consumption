import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# File paths for both datasets
file_path1 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/groundwater_energy_consumption_with_correcte_mean_stddev_berekening_per_pixel_script43.csv'
file_path2 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/groundwater_energy_consumption_with_correcte_mean_stddev_gem_heel_nederland_script44.csv'

# Load both datasets
df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

# Extract columns and convert from TWh to kWh by multiplying by 10^9 (dataset 1)
years1 = df1['Year']
energy_low1 = df1['Energy_Low_Efficiency_TWh_Calc_per_Pixel'] * 1e9
energy_high1 = df1['Energy_High_Efficiency_TWh_Calc_per_Pixel'] * 1e9
energy_low_upper1 = df1['Energy_Low_Efficiency_Upper_TWh_Calc_per_Pixel'] * 1e9
energy_low_lower1 = df1['Energy_Low_Efficiency_Lower_TWh_Calc_per_Pixel'] * 1e9
energy_high_upper1 = df1['Energy_High_Efficiency_Upper_TWh_Calc_per_Pixel'] * 1e9
energy_high_lower1 = df1['Energy_High_Efficiency_Lower_TWh_Calc_per_Pixel'] * 1e9

# Extract columns and convert from TWh to kWh by multiplying by 10^9 (dataset 2)
years2 = df2['Year']
energy_low2 = df2['Energy_Low_Efficiency_TWh_Calc_mean_NL'] * 1e9
energy_high2 = df2['Energy_High_Efficiency_TWh_Calc_mean_NL'] * 1e9
energy_low_upper2 = df2['Energy_Low_Efficiency_Upper_TWh_mean_NL'] * 1e9
energy_low_lower2 = df2['Energy_Low_Efficiency_Lower_TWh_mean_NL'] * 1e9
energy_high_upper2 = df2['Energy_High_Efficiency_Upper_TWh_mean_NL'] * 1e9
energy_high_lower2 = df2['Energy_High_Efficiency_Lower_TWh_mean_NL'] * 1e9

# Ensure yerr values are positive and ensure that lower bounds are not negative for both datasets
low_err_upper1 = np.abs(energy_low_upper1 - energy_low1)
low_err_lower1 = np.abs(np.maximum(0, energy_low1 - energy_low_lower1))
high_err_upper1 = np.abs(energy_high_upper1 - energy_high1)
high_err_lower1 = np.abs(np.maximum(0, energy_high1 - energy_high_lower1))

low_err_upper2 = np.abs(energy_low_upper2 - energy_low2)
low_err_lower2 = np.abs(np.maximum(0, energy_low2 - energy_low_lower2))
high_err_upper2 = np.abs(energy_high_upper2 - energy_high2)
high_err_lower2 = np.abs(np.maximum(0, energy_high2 - energy_high_lower2))

# Adjustable x-axis limits
xlim_start = 1980  # Start year for x-axis (adjustable)
xlim_end = 2016    # End year for x-axis (adjustable)

# Plot configuration (combined histogram)
fig, ax = plt.subplots(figsize=(16, 8))

# Plot histograms for low and high efficiency (dataset 1)
ax.bar(years1, energy_low1, width=-0.3, label='Low Efficiency (Pixel)', color='blue', align='edge', alpha=0.6)
ax.bar(years1, energy_high1, width=0.3, label='High Efficiency (Pixel)', color='green', align='edge', alpha=0.6)

# Plot histograms for low and high efficiency (dataset 2)
ax.bar(years2, energy_low2, width=-0.15, label='Low Efficiency (Mean NL)', color='cyan', align='edge', alpha=0.4)
ax.bar(years2, energy_high2, width=0.15, label='High Efficiency (Mean NL)', color='lightgreen', align='edge', alpha=0.4)

# Error bars for upper and lower limits (dataset 1)
ax.errorbar(years1, energy_low1, yerr=[low_err_lower1, low_err_upper1], fmt='o', color='blue', capsize=5, label='Low Efficiency Range (Pixel)')
ax.errorbar(years1, energy_high1, yerr=[high_err_lower1, high_err_upper1], fmt='o', color='green', capsize=5, label='High Efficiency Range (Pixel)')

# Error bars for upper and lower limits (dataset 2)
ax.errorbar(years2, energy_low2, yerr=[low_err_lower2, low_err_upper2], fmt='o', color='cyan', capsize=5, label='Low Efficiency Range (Mean NL)')
ax.errorbar(years2, energy_high2, yerr=[high_err_lower2, high_err_upper2], fmt='o', color='lightgreen', capsize=5, label='High Efficiency Range (Mean NL)')

# Titles and labels
ax.set_title('Energy Consumption for Groundwater Pumping in kWh (Combined Histogram View)')
ax.set_xlabel('Year')
ax.set_ylabel('Energy Consumption (kWh)')

# X-axis: show every 5th year (handling missing data better), but limit the number of labels
ax.set_xticks(np.arange(min(years1), max(years1) + 1, 1))  # Major ticks for every year
ax.set_xticks(np.arange(min(years1), max(years1) + 1, 5), minor=False)  # Only show labels every 5 years
ax.set_xticklabels(np.arange(min(years1), max(years1) + 1, 5), rotation=45)

# Apply x-axis limits (adjustable range)
ax.set_xlim([xlim_start, xlim_end])

# Apply log scale to y-axis
ax.set_yscale('log')

# Y-axis grid: major grid every power of 10, minor grid in between
ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=10))
ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=10))
ax.grid(which='both', color='gray', linestyle='-', linewidth=0.5)
ax.grid(which='minor', color='lightgray', linestyle='--', linewidth=0.5)

# X-axis grid: major grid every 5 years, minor grid in between
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.grid(which='major', axis='x', linestyle='-', linewidth=1)
ax.grid(which='minor', axis='x', linestyle='--', linewidth=0.5)

# Add legend
ax.legend()

# Display plot
plt.tight_layout()
plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# File path for energy consumption data
file_path_energy = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/observed_groundwater_energy_consumption_with_correcte_mean_stddev_2001_2021_script_45.csv'
df_energy = pd.read_csv(file_path_energy)

# Extract energy columns and convert from TWh to kWh by multiplying by 10^9
years_energy = df_energy['Year']
energy_low = df_energy['Energy_Low_Efficiency_TWh'] * 1e9
energy_high = df_energy['Energy_High_Efficiency_TWh'] * 1e9

# File path for precipitation data
file_path_precipitation = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/Irrigation_vs_precipitation_2001_2021.xlsx'

# Load the Excel file
xls = pd.ExcelFile(file_path_precipitation)

# Load Sheet3 (where precipitation data is stored)
df_precipitation = pd.read_excel(xls, sheet_name=2)

# Extract precipitation data (2001-2015 period)
years_precipitation = df_precipitation['Year']
precipitation = df_precipitation['Precipitation_NL_mm']

# Filter both energy and precipitation data for matching years (2001-2015)
years_filtered = years_energy[(years_energy >= 2001) & (years_energy <= 2015)]
energy_low_filtered = energy_low[(years_energy >= 2001) & (years_energy <= 2015)]
energy_high_filtered = energy_high[(years_energy >= 2001) & (years_energy <= 2015)]
precipitation_filtered = precipitation[(years_precipitation >= 2001) & (years_precipitation <= 2015)]

# Plot configuration (line chart for energy and bar chart for precipitation)
fig, ax1 = plt.subplots(figsize=(8, 8))

# Plot line for low and high efficiency
ax1.plot(years_filtered, energy_low_filtered, label='Pump Efficiency of 40%', color='blue', marker='o', linewidth=2)
ax1.plot(years_filtered, energy_high_filtered, label='Pump Efficiency of 70%', color='orange', marker='o', linewidth=2)

# Fill the area between low and high efficiency
ax1.fill_between(years_filtered, energy_low_filtered, energy_high_filtered, color='yellow', alpha=0.2, label='Efficiency Range')

# Titles and labels for the first y-axis
ax1.set_title('Energy Consumption for Groundwater Pumping [kWh] vs Precipitation [mm] \nwith Validated Irrigation Water Withdrawal (2001-2015)')
ax1.set_xlabel('Year')
ax1.set_ylabel('Energy Consumption [kWh]')

# X-axis: show every year, stopping at 2015
ax1.set_xticks(np.arange(2001, 2016, 1))
ax1.set_xticklabels(np.arange(2001, 2016, 1), rotation=45)

# Format the y-axis with scientific notation (e.g., 1e6 for 10^6)
ax1.yaxis.set_major_formatter(ticker.LogFormatterSciNotation())

# Add specific y-axis limits (for example, lower and upper bounds)
ax1.set_ylim([1e4, 1e7])

# Apply log scale to y-axis
ax1.set_yscale('log')

# Y-axis grid: major grid every power of 10, minor grid in between with 9 ticks
ax1.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=10))
ax1.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs='auto'))

# Disable minor ticks' labels but keep the lines for visual clarity
ax1.tick_params(which='minor', length=4, color='gray')

# Add gridlines and minor ticks for the first y-axis
ax1.grid(which='both', color='gray', linestyle='-', linewidth=0.5)
ax1.grid(which='minor', color='lightgray', linestyle='--', linewidth=0.5)

# Add legend for the energy consumption
ax1.legend(loc='upper left')

# ---------------- Add second y-axis for precipitation -----------------

# Create a second y-axis for precipitation
ax2 = ax1.twinx()
bar1 = ax2.bar(years_filtered, precipitation_filtered, color='lightblue', alpha=0.6, label='Precipitation [mm]', zorder=2)

# Labels for the second y-axis
ax2.set_ylabel('Precipitation [mm]', color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Set y-axis limits for precipitation
ax2.set_ylim([500, precipitation_filtered.max()])

# Add legend for the precipitation
bars_labels = [bar1]
labels_bars = ['Precipitation [mm]']
ax2.legend(bars_labels, labels_bars, loc='upper right')

# Display plot
plt.tight_layout()
plt.show()
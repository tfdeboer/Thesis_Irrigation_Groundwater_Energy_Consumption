import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Instellingen voor lettergrootte
label_fontsize = 15
title_fontsize = 22
legend_fontsize = 15
tick_fontsize = 13  # Grootte van de ticks op de as

# Logaritmische schaaloptie voor de y-as (True/False)
use_log_scale = True

# File path for observed energy consumption data
file_path_energy_observed = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/observed_groundwater_energy_consumption_with_correcte_mean_stddev_2001_2021_script_45.csv'
df_energy_observed = pd.read_csv(file_path_energy_observed)

# Extract energy columns for observed and convert from TWh to MWh
years_energy_observed = df_energy_observed['Year']
energy_low_observed = df_energy_observed['Energy_Low_Efficiency_TWh'] * 1e6  # Convert to MWh
energy_high_observed = df_energy_observed['Energy_High_Efficiency_TWh'] * 1e6  # Convert to MWh

# File path for energy consumption data (method 1)
file_path_energy_method_1 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/groundwater_energy_consumption_method_1.csv'
df_energy_method_1 = pd.read_csv(file_path_energy_method_1)

# Filter the data from 2001 to 2015 for method 1
df_energy_method_1_filtered = df_energy_method_1[(df_energy_method_1['Year'] >= 2001) & (df_energy_method_1['Year'] <= 2015)]
years_energy_method_1 = df_energy_method_1_filtered['Year']
energy_method_1_low = df_energy_method_1_filtered['Pump_Efficiency_40%_MWh']
energy_method_1_high = df_energy_method_1_filtered['Pump_Efficiency_70%_MWh']

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
years_filtered = years_energy_observed[(years_energy_observed >= 2001) & (years_energy_observed <= 2015)]
energy_low_observed_filtered = energy_low_observed[(years_energy_observed >= 2001) & (years_energy_observed <= 2015)]
energy_high_observed_filtered = energy_high_observed[(years_energy_observed >= 2001) & (years_energy_observed <= 2015)]
precipitation_filtered = precipitation[(years_precipitation >= 2001) & (years_precipitation <= 2015)]
energy_method_1_low_filtered = energy_method_1_low[(years_energy_method_1 >= 2001) & (years_energy_method_1 <= 2015)]
energy_method_1_high_filtered = energy_method_1_high[(years_energy_method_1 >= 2001) & (years_energy_method_1 <= 2015)]

# Plot configuration (line chart for energy and bar chart for precipitation)
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot line for low and high efficiency for method 1 data
ax1.plot(years_filtered, energy_method_1_low_filtered, label='M1: Modelled Withdrawal (Eff. 40%)', color='green', linestyle='-', marker='x', linewidth=2)
ax1.plot(years_filtered, energy_method_1_high_filtered, label='M1: Modelled Withdrawal (Eff. 70%)', color='red', linestyle='-', marker='x', linewidth=2)

# Fill the area between low and high efficiency for method 1 data
ax1.fill_between(years_filtered, energy_method_1_low_filtered, energy_method_1_high_filtered, color='lightgreen', alpha=0.2, label='Modelled Efficiency Range')

# Plot line for low and high efficiency for observed data
ax1.plot(years_filtered, energy_low_observed_filtered, label='M2: Observed Withdrawal (Eff. 40%)', color='blue', marker='o', linewidth=2)
ax1.plot(years_filtered, energy_high_observed_filtered, label='M2: Observed Withdrawal (Eff. 70%)', color='orange', marker='o', linewidth=2)

# Fill the area between low and high efficiency for observed data
ax1.fill_between(years_filtered, energy_low_observed_filtered, energy_high_observed_filtered, color='yellow', alpha=0.2, label='Observed Efficiency Range')

# Titles and labels for the first y-axis
ax1.set_title('Energy Consumption for Groundwater Pumping [MWh] vs Precipitation [mm] \nfor Modelled and Observed Irrigation Water Withdrawal (2001-2015)', fontsize=title_fontsize)
ax1.set_xlabel('Year', fontsize=label_fontsize)
ax1.set_ylabel('Energy Consumption [MWh]', fontsize=label_fontsize)

# X-axis: show every year, stopping at 2015
ax1.set_xticks(np.arange(2001, 2016, 1))
ax1.set_xticklabels(np.arange(2001, 2016, 1), rotation=45, fontsize=tick_fontsize)

# Y-axis: customize tick labels for readability
ax1.tick_params(axis='y', labelsize=tick_fontsize)

# Add gridlines and minor ticks for the first y-axis
ax1.grid(which='both', color='gray', linestyle='-', linewidth=0.5)
ax1.grid(which='minor', color='lightgray', linestyle='--', linewidth=0.5)

# Set y-axis scale to log if enabled
if use_log_scale:
    ax1.set_yscale('log')

# Move the legend outside the main plot area
legend = ax1.legend(fontsize=legend_fontsize, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

# ---------------- Add second y-axis for precipitation -----------------

# Create a second y-axis for precipitation
ax2 = ax1.twinx()
bar1 = ax2.bar(years_filtered, precipitation_filtered, color='lightblue', alpha=0.6, label='Precipitation [mm]', zorder=2)

# Labels for the second y-axis
ax2.set_ylabel('Precipitation [mm]', fontsize=label_fontsize)
ax2.tick_params(axis='y', labelsize=tick_fontsize)

# Set y-axis limits for precipitation
ax2.set_ylim([500, precipitation_filtered.max()])

# Add legend for the precipitation
bars_labels = [bar1]
labels_bars = ['Precipitation [mm]']
ax2.legend(bars_labels, labels_bars, loc='upper right', fontsize=legend_fontsize)

# Adjust layout to fit the new legend position
plt.tight_layout()
plt.subplots_adjust(bottom=0.3)  # Adjust the bottom space to fit the legend below the figure
plt.show()
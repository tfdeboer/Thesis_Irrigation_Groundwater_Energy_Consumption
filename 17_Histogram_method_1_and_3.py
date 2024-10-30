import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# File paths
file_method_1 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/groundwater_energy_consumption_method_1.csv'
file_method_2 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/groundwater_energie_consumptions_method_3_2001_2015.csv'

# Load data from both methods
df_method_1 = pd.read_csv(file_method_1)
df_method_2 = pd.read_csv(file_method_2)

# Select the columns for year and energy consumption with different efficiencies
years_method_1 = df_method_1['Year']
energy_55_method_1 = df_method_1['Pump_Efficiency_55%_MWh']
energy_40_method_1 = df_method_1['Pump_Efficiency_40%_MWh']
energy_70_method_1 = df_method_1['Pump_Efficiency_70%_MWh']

years_method_2 = df_method_2['Year']
energy_55_method_2 = df_method_2['Pump_Efficiency_55%_MWh']
energy_40_method_2 = df_method_2['Pump_Efficiency_40%_MWh']
energy_70_method_2 = df_method_2['Pump_Efficiency_70%_MWh']

# Calculate absolute error bars for each method
lower_error_method_1 = energy_55_method_1 - energy_70_method_1  # Lower bound: Difference from 55% to 70%
upper_error_method_1 = energy_40_method_1 - energy_55_method_1  # Upper bound: Difference from 55% to 40%
error_bars_method_1 = [lower_error_method_1, upper_error_method_1]

lower_error_method_2 = energy_55_method_2 - energy_70_method_2
upper_error_method_2 = energy_40_method_2 - energy_55_method_2
error_bars_method_2 = [lower_error_method_2, upper_error_method_2]

# Plotting parameters
bar_width = 0.35
fig, ax = plt.subplots(figsize=(16, 8))

# Create bars for method 1 (shifted slightly to the left)
bars_method_1 = ax.bar(
    years_method_1 - bar_width/2, 
    energy_55_method_1, 
    width=bar_width, 
    yerr=error_bars_method_1, 
    capsize=5, 
    label='Method 1 (55% Efficiency)', 
    color='skyblue', 
    alpha=0.7,
    error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2)  # Customize error bar appearance
)

# Create bars for method 2 (shifted slightly to the right)
bars_method_2 = ax.bar(
    years_method_2 + bar_width/2, 
    energy_55_method_2, 
    width=bar_width, 
    yerr=error_bars_method_2, 
    capsize=5, 
    label='Method 2 (55% Efficiency)', 
    color='lightgreen', 
    alpha=0.7,
    error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2)
)

# Labels and Title
ax.set_xlabel('Year', fontsize=16)
ax.set_ylabel('Energy Consumption [MWh]', fontsize=16)
ax.set_title('Comparison of Groundwater Pump Energy Consumption for Irrigation\nMethods 1 and 2 (1980-2015)', fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=14)

# Set x-axis limits to show years from 1980 to 2015
ax.set_xlim([1980, 2016])

# Add gridlines for better readability
ax.grid(True, linestyle='--', alpha=0.5)

# Show the legend
ax.legend(fontsize=14)

# Show plot
plt.tight_layout()
plt.show()
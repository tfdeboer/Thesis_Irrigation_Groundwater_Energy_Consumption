import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LogLocator, LogFormatterMathtext

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

# Customize plot styles
bar_width = 0.4
fig, ax = plt.subplots(figsize=(16, 10))

# Plot bars for method 1 (shifted slightly to the left)
bars_method_1 = ax.bar(
    years_method_1 - bar_width/2, 
    energy_55_method_1, 
    width=bar_width, 
    yerr=error_bars_method_1, 
    capsize=5, 
    label='Method 1 (55% Efficiency)', 
    color='blue', 
    alpha=0.7,
    error_kw=dict(ecolor='black', lw=2, capsize=5, capthick=2)  # Customize error bar appearance
)

# Plot bars for method 2 (shifted slightly to the right)
bars_method_2 = ax.bar(
    years_method_2 + bar_width/2, 
    energy_55_method_2, 
    width=bar_width, 
    yerr=error_bars_method_2, 
    capsize=5, 
    label='Method 2 (55% Efficiency)', 
    color='darkgreen', 
    alpha=0.7,
    error_kw=dict(ecolor='black', lw=2, capsize=5, capthick=2)
)

# Set log scale on y-axis and adjust limits
ax.set_yscale('log')
ax.set_ylim([1e-3, 2e3])  # Set y-axis range to start from 10^-3 to better show the data

# Labels and title (adjustable font sizes)
font_size_axes = 20
font_size_labels = 22
font_size_title = 30
font_size_legend = 23
font_size_ticks = 20

# Set labels and title
ax.set_xlabel('Year', fontsize=font_size_axes)
ax.set_ylabel('Energy Consumption [MWh]', fontsize=font_size_axes)
ax.set_title('Comparison of Groundwater Pump Energy Consumption for Irrigation\nMethods 1 and 2 (1980-2015)', fontsize=font_size_title)

# Set tick parameters
ax.tick_params(axis='both', which='major', labelsize=font_size_ticks)

# Adjust x-axis limits to the specified range
ax.set_xlim([1980, 2016])

# Customize x-ticks to show labels every 5 years and add small tick marks for each year
ax.set_xticks(np.arange(1980, 2016, 5))  # Major ticks and labels every 5 years
ax.set_xticklabels(np.arange(1980, 2016, 5), fontsize=font_size_ticks)  # Set labels for every 5 years
ax.set_xticks(np.arange(1980, 2016, 1), minor=True)  # Minor ticks for every year (small streepjes)

# Customize appearance of the minor ticks
ax.tick_params(axis='x', which='minor', length=6, width=1.5, color='grey')  # Small streepjes on x-axis

# Customize y-axis with a log scale, logarithmic gridlines, and scientific notation
ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=10))  # Major ticks at powers of 10
ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=[2, 3, 4, 5, 6, 7, 8, 9]))  # Minor ticks at intermediate values
ax.yaxis.set_major_formatter(LogFormatterMathtext())  # Use scientific notation with 10^{x}

# Add gridlines with lighter colors
ax.grid(True, which='both', linestyle='--', linewidth=0.75, color='lightgray', alpha=0.7)  # Minor gridlines
ax.grid(True, which='major', linestyle='-', linewidth=0.75, color='gray', alpha=0.9)  # Major gridlines

# Update legend with error bar information
ax.legend(['Method 1 (Model Withdrawals) - Error bars (40%-70% Pump Efficiency)', 
           'Method 2 (Observed Withdrawals) - Error bars (40%-70% Pump Efficiency)'], 
          fontsize=font_size_legend)

# Show plot with tight layout
plt.tight_layout()
plt.show()
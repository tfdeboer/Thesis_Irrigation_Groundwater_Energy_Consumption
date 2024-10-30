import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Instellingen voor lettergrootte
title_fontsize = 26
axis_label_fontsize = 22
tick_label_fontsize = 22
legend_fontsize = 22

# File path for the total energy consumption data
file_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/Total_results_energy_consumptions.csv'
df_total = pd.read_csv(file_path)

# File path for the energy consumption per different models
file_energy_per_pixel = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/Total_results_energy_consumptions.csv'
file_energy_observed = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/Total_results_energy_consumptions.csv'

df_pixel = pd.read_csv(file_energy_per_pixel)
df_observed = pd.read_csv(file_energy_observed)

# Merging data on 'Year' for easier plotting
df_merged = pd.merge(df_total[['Year', 'Total electricity (TWh)']], 
                     df_pixel[['Year', 'Energy_Low_Efficiency_TWh_Calc_per_Pixel', 'Energy_High_Efficiency_TWh_Calc_per_Pixel']], 
                     on='Year', how='left')
df_merged = pd.merge(df_merged, 
                     df_observed[['Year', 'Energy_Low_Efficiency_TWh_observed', 'Energy_High_Efficiency_TWh_observed']], 
                     on='Year', how='left')

# Calculate percentage of total energy consumption for each method
df_merged['Pixel_Low_Percentage'] = (df_merged['Energy_Low_Efficiency_TWh_Calc_per_Pixel'] / df_merged['Total electricity (TWh)']) * 100
df_merged['Pixel_High_Percentage'] = (df_merged['Energy_High_Efficiency_TWh_Calc_per_Pixel'] / df_merged['Total electricity (TWh)']) * 100
df_merged['Observed_Low_Percentage'] = (df_merged['Energy_Low_Efficiency_TWh_observed'] / df_merged['Total electricity (TWh)']) * 100
df_merged['Observed_High_Percentage'] = (df_merged['Energy_High_Efficiency_TWh_observed'] / df_merged['Total electricity (TWh)']) * 100

# Create a DataFrame for the CSV output
output_df = pd.DataFrame({
    'Year': df_merged['Year'],
    'Model_Withdrawal_40%_Efficiency (%)': df_merged['Pixel_Low_Percentage'],
    'Model_Withdrawal_70%_Efficiency (%)': df_merged['Pixel_High_Percentage'],
    'Observed_Withdrawal_40%_Efficiency (%)': df_merged['Observed_Low_Percentage'],
    'Observed_Withdrawal_70%_Efficiency (%)': df_merged['Observed_High_Percentage']
})

# Save the table as a CSV file
output_csv_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/Irrigation_Pumping_Efficiency_Percentage.csv'
output_df.to_csv(output_csv_path, index=False)

# Plotting configuration
fig, ax = plt.subplots(figsize=(10, 6))

# Plot for Method 1: Calculation with Groundwater Head per Pixel
ax.fill_between(df_merged['Year'], df_merged['Pixel_Low_Percentage'], df_merged['Pixel_High_Percentage'], 
                color='green', alpha=0.2, label='Method 1: Model Withdrawals')
ax.plot(df_merged['Year'], df_merged['Pixel_Low_Percentage'], color='green', linestyle='--')
ax.plot(df_merged['Year'], df_merged['Pixel_High_Percentage'], color='green')

# Plot for new Method 2: Observed Irrigation Water Withdrawals
ax.fill_between(df_merged['Year'], df_merged['Observed_Low_Percentage'], df_merged['Observed_High_Percentage'], 
                color='orange', alpha=0.2, label='Method 2: Observed Withdrawals')
ax.plot(df_merged['Year'], df_merged['Observed_Low_Percentage'], color='orange', linestyle='--')
ax.plot(df_merged['Year'], df_merged['Observed_High_Percentage'], color='orange')

# Titles and labels with customizable font sizes
ax.set_title('Energy Consumption for Irrigation Pumping as a Percentage of Total Electricity Usage in NL [MWh]', fontsize=title_fontsize)
ax.set_xlabel('Year', fontsize=axis_label_fontsize)
ax.set_ylabel('Percentage of Total Electricity Consumption (%)', fontsize=axis_label_fontsize)

# X-axis configuration
ax.set_xticks(np.arange(1980, 2022, 5))  # Show every 5 years as major ticks
ax.set_xlim([1980, 2016])  # Stop the x-axis at 2015
ax.tick_params(axis='x', labelsize=tick_label_fontsize)

# **Add minor ticks for each year**
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))  # Minor ticks every 1 year
ax.tick_params(axis='x', which='minor', length=5, color='gray')  # Customize the appearance of minor ticks

# Y-axis configuration with logarithmic scale
ax.set_ylim([1e-9, 2.5e-3])  # Adjust y-axis limits for log scale
ax.set_yscale('log')  # Set y-axis to log scale
ax.yaxis.set_major_formatter(ticker.LogFormatterSciNotation())  # Format the y-axis labels for scientific notation
ax.tick_params(axis='y', labelsize=tick_label_fontsize)

# Add gridlines for the plot
ax.grid(which='both', color='gray', linestyle='-', linewidth=0.5)
ax.grid(which='minor', color='lightgray', linestyle='--', linewidth=0.5)

# Add a legend with customizable font size
plt.legend(fontsize=legend_fontsize, loc='upper left')

# Display the plot
plt.tight_layout()
plt.show()

print(f"Output table saved as: {output_csv_path}")
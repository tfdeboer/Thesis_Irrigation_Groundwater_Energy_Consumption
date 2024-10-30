import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Path to your Excel file
file_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/Irrigation_vs_precipitation_2001_2021.xlsx'

# Load the Excel file
xls = pd.ExcelFile(file_path)

# Load Sheet3 (where all data is stored)
df = pd.read_excel(xls, sheet_name=2)

# Extract relevant columns from Sheet3
years = df['Year']
irrigation = df['Grondwater_irrigatie_m^3']
precipitation = df['Precipitation_NL_mm']
total_withdrawal_model = df['Total_Withdrawal_m3_model']

# Create a plot with three y-axes
fig, ax1 = plt.subplots(figsize=(15, 9))

# Plot irrigation as a bar chart on the first y-axis
bar1 = ax1.bar(years, irrigation, color='lightblue', label='Groundwater for Irrigation', alpha=0.5, zorder=1)

# Set x and y labels for ax1
ax1.set_xlabel('Year')
ax1.set_ylabel('Groundwater Withdrawals [m³]', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Set y-axis tick format for irrigation
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Create a second y-axis for precipitation (line plot)
ax2 = ax1.twinx()
line_precipitation, = ax2.plot(years, precipitation, color='blue', label='Precipitation [mm]', linewidth=2, linestyle='-', zorder=3)
ax2.set_ylabel('Precipitation [mm]', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Set y-axis limits and format for precipitation
ax2.set_ylim([500, precipitation.max()])
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Create a third y-axis for the 'Total_Withdrawal_m3_model' using a different scale
ax3 = ax1.twinx()

# Offset the third y-axis so it doesn't overlap
ax3.spines['right'].set_position(('outward', 60))  # Offset by 60 points

# Plot 'Total_Withdrawal_m3_model' as a bar chart
bar2 = ax3.bar(years, total_withdrawal_model, color='green', label='Groundwater Withdrawal (Model)', alpha=0.6, zorder=2)

# Set the y-axis label for the third axis and formatting
ax3.set_ylabel('Groundwater Withdrawal (Model) [m³]', color='green')
ax3.tick_params(axis='y', labelcolor='green')
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Add gridlines (both horizontal and vertical)
ax1.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)  # Horizontal gridlines
ax1.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)  # Vertical gridlines

# Add title and labels
plt.title('Comparison of Groundwater Withdrawals (Observed & Model) and Precipitation (1980-2021)')

# Add legend for all the elements (both bars and line)
bars_labels = [bar1, bar2]
lines_labels = [line_precipitation]
labels_bars = ['Groundwater for Irrigation [m³]', 'Groundwater Withdrawal (Model) [m³]']
labels_lines = ['Precipitation [mm]']

# Combine bars and line in the legend
ax1.legend(bars_labels + lines_labels, labels_bars + labels_lines, loc='upper left', bbox_to_anchor=(1, 1))

# Adjust the layout to make space for the legend
plt.tight_layout(rect=[0, 0, 0.85, 1])

# Show the plot
plt.show()
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
irrigation = df['Grondwater_irrigatie_m^3'] / 1_000_000  # Convert to millions
precipitation = df['Precipitation_NL_mm']
total_withdrawal_model = df['Total_Withdrawal_m3_model'] / 1_000_000  # Convert to millions

# Create a plot with two y-axes
fig, ax1 = plt.subplots(figsize=(15, 9))

# Increase font sizes for axes, labels, and title
font_size_axes = 18
font_size_labels = 22
font_size_title = 24
font_size_legend = 18

# Plot the 'Grondwater_irrigatie_m^3' on the first y-axis (solid line)
line1, = ax1.plot(years, irrigation, color='darkblue', label='Groundwater Withdrawal (Observed by vd Meer, 2023)', linewidth=2, linestyle='-', zorder=2)

# Plot the 'Total_Withdrawal_m3_model' on the first y-axis (dashed line)
line2, = ax1.plot(years, total_withdrawal_model, color='green', label='Groundwater Withdrawal (Calculated by Model)', linewidth=2, linestyle='--', zorder=2)

# Set labels and format for x and y axes
ax1.set_xlabel('Year', fontsize=font_size_labels)
ax1.set_ylabel('Groundwater Withdrawals [Million m³]', fontsize=font_size_labels, color='black')
ax1.tick_params(axis='y', labelcolor='black', labelsize=font_size_axes)
ax1.tick_params(axis='x', labelsize=font_size_axes)

# Adjust x-axis to only show the years between 1980 and 2020
ax1.set_xlim([1980, 2021])

# Create a second y-axis for precipitation
ax2 = ax1.twinx()
bar1 = ax2.bar(years, precipitation, color='lightblue', alpha=0.6, label='Precipitation [mm]', zorder=2)
ax2.set_ylabel('Precipitation [mm]', fontsize=font_size_labels, color='black')
ax2.tick_params(axis='y', labelcolor='black', labelsize=font_size_axes)

# Set y-axis limits for precipitation
ax2.set_ylim([500, precipitation.max()])

# Add gridlines (both horizontal and vertical)
ax1.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)  # Horizontal gridlines
ax1.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)  # Vertical gridlines

# Set y-axis tick format for irrigation (showing values in millions)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}'))

# Add title and labels with increased font size
plt.title('Comparison of Observed and Modeled Groundwater Withdrawals for Irrigation in Relation to Precipitation (1980-2021)', fontsize=font_size_title)

# Add legend for both the lines and the bars
lines_labels = [line1, line2]
bars_labels = [bar1]
labels_lines = [line1.get_label(), line2.get_label()]
labels_bars = ['Precipitation [mm]']

# Combine lines and bars in the legend with a larger font size
ax1.legend(lines_labels + bars_labels, labels_lines + labels_bars, loc='upper left', fontsize=font_size_legend)

# Adjust the layout to prevent label overlap
plt.tight_layout()

# Show the plot
plt.show()
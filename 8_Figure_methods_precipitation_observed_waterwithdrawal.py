import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Parameters voor visualisatie-instellingen
circle_size = 10  # Pas de cirkelgrootte aan (niet van toepassing in deze plot)
title_font_size = 26  # Lettergrootte van de titel
axis_label_font_size = 22  # Lettergrootte van de aslabels
tick_font_size = 20  # Lettergrootte van de x- en y-as getallen
colorbar_tick_size = 18  # Lettergrootte voor de getallen op de schaalbalk (niet van toepassing hier)
legend_label = 'Mean Groundwater Depth [m]'  # Legenda label (niet van toepassing hier)

# Path to your Excel file
file_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/Irrigation_vs_precipitation_2001_2021.xlsx'

# Load the Excel file
xls = pd.ExcelFile(file_path)

# Load Sheet3 (where all data is stored)
df = pd.read_excel(xls, sheet_name=2)

# Extract relevant columns from Sheet3
years = df['Year']
irrigation = df['Grondwater_irrigatie_m^3'] / 1_000_000  # Omzetten naar miljoenen kubieke meters
precipitation = df['Precipitation_NL_mm']

# Create a plot with two y-axes
fig, ax1 = plt.subplots(figsize=(15, 9))

# Plot the 'Grondwater_irrigatie_m^3' on the first y-axis (solid line)
line1, = ax1.plot(years, irrigation, color='darkblue', label='Groundwater Withdrawal (Observed by vd Meer, 2023)', linewidth=2, linestyle='-', zorder=2)

# Weghalen van de groene lijn (Calculated by Model)

# Configureer de eerste y-as
ax1.set_xlabel('Year', fontsize=axis_label_font_size)
ax1.set_ylabel('Groundwater Withdrawal [Million m³]', color='black', fontsize=axis_label_font_size)  # Aanpassing van het label
ax1.tick_params(axis='y', labelcolor='black', labelsize=tick_font_size)

# Adjust x-axis to only show the years between 1980 and 2020
ax1.set_xlim([1980, 2021])
ax1.tick_params(axis='x', labelsize=tick_font_size)

# Create a second y-axis for precipitation
ax2 = ax1.twinx()
bar1 = ax2.bar(years, precipitation, color='lightblue', alpha=0.6, label='Precipitation [mm]', zorder=2)
ax2.set_ylabel('Precipitation [mm]', color='black', fontsize=axis_label_font_size)
ax2.tick_params(axis='y', labelcolor='black', labelsize=tick_font_size)

# Set y-axis limits for precipitation
ax2.set_ylim([500, precipitation.max()])

# Add gridlines (both horizontal and vertical)
ax1.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)  # Horizontal gridlines
ax1.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)  # Vertical gridlines

# Set y-axis tick format for irrigation (with comma separators in millions)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Add title and labels met lettergroottes
plt.title('Comparison of Observed Groundwater Withdrawal for \nIrrigation in Relation to Precipitation (1980-2021)', fontsize=title_font_size)

# Add legend for the line and the bars
lines_labels = [line1]
bars_labels = [bar1]
labels_lines = [line1.get_label()]
labels_bars = ['Precipitation [mm]']

# Combine lines and bars in the legend
ax1.legend(lines_labels + bars_labels, labels_lines + labels_bars, loc='upper left', fontsize=tick_font_size)

# Adjust the layout
plt.tight_layout()

# Show the plot
plt.show()
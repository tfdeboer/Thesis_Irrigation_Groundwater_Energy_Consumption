import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Bestandspaden
input_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/Lizard_PDOK_all_data_wells_with_WGS84_nearest_Well_id_with_thickness_with_layer.csv'
shapefile = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'
output_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/Lizard_PDOK_all_data_wells_with_1980_2015_data.csv'

# Parameters voor visualisatie-instellingen
circle_size = 5  # Pas de cirkelgrootte aan
title_font_size = 26  # Lettergrootte van de titel
axis_label_font_size = 22  # Lettergrootte van de aslabels
tick_font_size = 14  # Lettergrootte van de x- en y-as getallen
legend_label = 'Missing Data Percentage [%]'  # Legenda label
colorbar_tick_size = 22  # Lettergrootte voor de getallen op de schaalbalk

# Data inladen
df = pd.read_csv(input_file)

# Datum kolommen naar datetime-formaat converteren
df['time_range_start'] = pd.to_datetime(df['time_range_start'], format='%d/%m/%Y', errors='coerce')
df['time_range_end'] = pd.to_datetime(df['time_range_end'], format='%d/%m/%Y', errors='coerce')

# Bereken het aantal maanden en het percentage voor 1980-2015
def calculate_missing_percentage(start_date, end_date, start_period='1980-01-01', end_period='2015-12-31'):
    start_period = pd.to_datetime(start_period)
    end_period = pd.to_datetime(end_period)

    if pd.isna(start_date) or pd.isna(end_date):
        return None, None  # Geen data beschikbaar

    # Zorg dat de data binnen de range valt
    adjusted_start = max(start_date, start_period)
    adjusted_end = min(end_date, end_period)

    # Controleer of er overlap is met de periode 1980-2015
    if adjusted_start > adjusted_end:
        return None, None

    # Bereken het aantal beschikbare maanden
    total_months = 12 * (end_period.year - start_period.year + 1)
    available_months = (adjusted_end.year - adjusted_start.year) * 12 + (adjusted_end.month - adjusted_start.month) + 1

    missing_percentage = 100 - (available_months / total_months * 100)
    return available_months, missing_percentage

# Nieuwe kolommen berekenen
df[['num_months_1980_2015', 'missing_percentage_1980_2015']] = df.apply(
    lambda row: calculate_missing_percentage(row['time_range_start'], row['time_range_end']),
    axis=1, result_type='expand'
)

# Filter rijen zonder data in de nieuwe periode
df = df.dropna(subset=['missing_percentage_1980_2015'])

# Opslaan in een nieuw CSV-bestand
df.to_csv(output_file, index=False)
print(f"Data met missing_percentage_1980_2015 opgeslagen in: {output_file}")

# Gegevens voor de plot voorbereiden
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['x_WGS84'], df['y_WGS84']), crs="EPSG:4326")

# Laad shapefile van de provincies
province_gdf = gpd.read_file(shapefile)

# Plot de kaart
fig, ax = plt.subplots(figsize=(12, 8))
province_gdf.plot(ax=ax, color='white', edgecolor='black')

# Plot de well data met aangepaste kleurenschaal en volledige schaal (0-100%)
vmin, vmax = 0, 100  # Zorg ervoor dat de schaal van de kleurenbalk 0-100% is
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
cmap = cm.coolwarm
gdf.plot(ax=ax, column='missing_percentage_1980_2015', cmap=cmap, markersize=circle_size, norm=norm)

# Handmatig een kleurenbalk toevoegen
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label(legend_label, fontsize=axis_label_font_size)

# Pas de lettergrootte van de tick labels op de kleurenschaal aan
cbar.ax.tick_params(labelsize=colorbar_tick_size)

# Titel en labels instellen
plt.title('Missing Data Percentage \n(1980-2015) per Well', fontsize=title_font_size)
plt.xlabel('Longitude', fontsize=axis_label_font_size)
plt.ylabel('Latitude', fontsize=axis_label_font_size)

# Pas de lettergrootte van de tick labels aan
ax.tick_params(axis='both', which='major', labelsize=tick_font_size)

# Voeg grid toe en visualiseer de kaart
plt.grid(True)
plt.show()
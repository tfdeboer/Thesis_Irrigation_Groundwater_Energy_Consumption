import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# Parameters voor visualisatie-instellingen
title_font_size = 24  # Lettergrootte van de titel
axis_label_font_size = 20  # Lettergrootte van de aslabels
tick_font_size = 16  # Lettergrootte van de x- en y-as getallen
colorbar_label_size = 22  # Lettergrootte van het kleurenschaallabel
colorbar_tick_size = 20  # Lettergrootte voor de getallen op de kleurenschaal

# File paths
nc_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/data/nc/NL/globgm_bottom_5arcmin_monthly_1958_2015_netherlands.nc'
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'

# Probeer het NetCDF-bestand te laden
try:
    ds = xr.open_dataset(nc_file)
    print("NetCDF-bestand succesvol ingeladen.")
except FileNotFoundError:
    print(f"Error: Het bestand {nc_file} is niet gevonden. Controleer het pad en probeer opnieuw.")
    exit(1)

# Bekijk de structuur van de dataset om de juiste variabele te identificeren
print(ds)

# Selecteer de tijdsperiode 1980-2015 en de juiste variabele (grondwaterstand)
ds_period = ds.sel(time=slice("1980-01-01", "2015-12-31"))

# Selecteer de `groundwater_depth` variabele en verwijder de `region` dimensie
mean_gw_level = ds_period['groundwater_depth'].sel(region=0).mean(dim='time')

# Laad de shapefile
shapefile = gpd.read_file(shapefile_path)

# Plot de gemiddelde grondwaterstanden met de opgegeven stijl
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': ccrs.PlateCarree()})  # Kleinere figuur

# Voeg de shapefile toe aan de plot
shapefile.plot(ax=ax, edgecolor='black', facecolor='lightgrey', alpha=0.6)

# Plot de gemiddelde grondwaterstand met aangepaste opmaak
contour = mean_gw_level.plot(
    ax=ax,
    cmap='terrain',
    add_colorbar=False,
    vmin=0,  # Minimale waarde voor de colorbar
    vmax=50  # Maximale waarde voor de colorbar
)

# Handmatig toevoegen van de colorbar onderaan de figuur met vloeiende overgang
cbar = plt.colorbar(
    contour,
    ax=ax,
    orientation='horizontal',
    fraction=0.05,
    pad=0.1,
    aspect=30  # Verhouding van de lengte/hoogte
)

# Stel de ticks handmatig in voor een continue schaal
cbar.set_ticks([0, 10, 20, 30, 40, 50])
cbar.set_label('Groundwater Depth [m]', fontsize=colorbar_label_size)  # Lettergrootte van het label
cbar.ax.tick_params(labelsize=colorbar_tick_size)  # Grootte van de ticks op de schaal

# Pas de stijl van de titel en de labels aan
ax.set_title('Bottom Layer', fontsize=title_font_size, pad=20)
ax.set_xlabel('Longitude', fontsize=axis_label_font_size, labelpad=10)
ax.set_ylabel('Latitude', fontsize=axis_label_font_size, labelpad=10)

# Pas de ticks en ticklabels aan
ax.tick_params(axis='both', which='major', labelsize=tick_font_size)

# Voeg gridlines toe voor een duidelijkere visualisatie
gridlines = ax.gridlines(draw_labels=True, linestyle="--", linewidth=0.5, color='gray')
gridlines.xlabels_top = False
gridlines.ylabels_right = False
gridlines.xformatter = LongitudeFormatter()  # Gebruik cartopy's LongitudeFormatter
gridlines.yformatter = LatitudeFormatter()  # Gebruik cartopy's LatitudeFormatter
gridlines.xlabel_style = {'size': tick_font_size}
gridlines.ylabel_style = {'size': tick_font_size}

# Voeg kustlijnen en grenzen toe
ax.add_feature(cfeature.COASTLINE, linewidth=1.0)
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=1.0)

# Toon de plot met alle aanpassingen
plt.tight_layout()
plt.show()
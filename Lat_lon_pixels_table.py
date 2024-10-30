import xarray as xr

#Open NetCDF-file
nc_file_path = "/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/globgm_bottom_5arcmin_monthly_1958_2015_netherlands.nc"
dataset = xr.open_dataset(nc_file_path)
print(dataset)

#Haal de latitudes en longitudes op
lat = dataset["lat"].values
lon = dataset["lon"].values

import numpy as np

# Maak een 2D meshgrid voor latitudes en longitudes
lat_mesh, lon_mesh = np.meshgrid(lat, lon, indexing='ij')

print("Latitudes;")
print(lat_mesh)

print("Longitudes")
print(lon_mesh)

#Combineer de coördinaten
coordinates = np.stack([lat_mesh, lon_mesh], axis=-1)

print("Coordinates of every pixel:")
print(coordinates)

##############################################


import pandas as pd

# Maak een DataFrame waarbij de rijen en kolommen overeenkomen met de meshgrids
rows, cols, _ = coordinates.shape
data = pd.DataFrame(index=range(rows), columns=range(cols))

# Vul de DataFrame met de tuples van latitude en longitude
for i in range(rows):  # Doorloop de rijen
    for j in range(cols):  # Doorloop de kolommen
        lat = lat_mesh[i, j]
        lon = lon_mesh[i, j]
        data.loc[i, j] = (lat, lon)  # Voeg de tuple toe aan de juiste cel

print(data)  # Bekijk de DataFrame met lat/lon tuples

# Exporteer naar een CSV-bestand
csv_path = "latitude_longitude_grid.csv"
data.to_csv(csv_path, index=True)  # Sla de DataFrame op als CSV

print(f"DataFrame opgeslagen naar {csv_path}")

# Exporteer naar een Excel-bestand (voor betere leesbaarheid van tuples)
excel_path = "latitude_longitude_grid.xlsx"
data.to_excel(excel_path, index=True)

print(f"DataFrame opgeslagen naar {excel_path}")
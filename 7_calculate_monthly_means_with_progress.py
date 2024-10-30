import pickle
import pandas as pd
import xarray as xr

# Inlezen van het .pklz-bestand
input_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/gw_bro_Netherlands.pklz'
output_directory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/output/Observed_data/Mean_CDO/'

with open(input_file, 'rb') as f:
    gw_bro = pickle.load(f)

# Data filteren op de periode 1958 t/m 2015
start_date = pd.Timestamp('1958-01-01')
end_date = pd.Timestamp('2015-12-31')

# Functie om de gemiddelde waterstand in de periode te berekenen
def mean_water_level_in_period(obs, start_date, end_date):
    period_data = obs[(obs.index >= start_date) & (obs.index <= end_date)]
    if not period_data.empty:
        return period_data['value'].mean()
    else:
        return None

# Initialiseren van lijsten voor gemiddelde waterstanden en locaties
data = []

# Itereren door de rijen om de gemiddelde waterstand te berekenen
for index, row in gw_bro.iterrows():
    x = row['x']
    y = row['y']
    time_series_data = row['obs']
    if not time_series_data.empty:
        time_series_data = pd.DataFrame(time_series_data)
        time_series_data.index = pd.to_datetime(time_series_data.index)  # Zet de index om naar datetime
        time_series_data.columns = ['value', 'flag', 'comment']  # Pas de kolomnamen aan naar behoefte
        for date, value in time_series_data['value'].items():
            data.append({'time': date, 'x': x, 'y': y, 'value': value})

# Zet de data om naar een pandas DataFrame
df = pd.DataFrame(data)

# Zet de DataFrame om naar een xarray Dataset
ds = df.set_index(['time', 'x', 'y']).to_xarray()

# Sla het netCDF-bestand op
netcdf_file = output_directory + 'gw_bro_Netherlands.nc'
ds.to_netcdf(netcdf_file)

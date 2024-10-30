import netCDF4 as nc
import numpy as np

# Define the file path
nc_file_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/nc/irrGWWW_m3_year_1960_2019_NL.nc'

# Load the NetCDF file
ds = nc.Dataset(nc_file_path)

# Access the 'time' variable
time_var = ds.variables['time']

# Print the number of time steps available
print(f"Number of years available: {len(time_var)}")

# Convert the time variable to a readable format, assuming it's in a standard calendar format
years = nc.num2date(time_var[:], units=time_var.units)

# Print the years
print("Available years:", years)

# Alternatively, just print the unique years if they are directly stored
# print("Available years:", np.unique(time_var[:]))

import os
import pandas as pd

# Paths to directories
input_dir = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input'
well_ids_file = os.path.join(input_dir, 'well_ids_GLD_PDOK.txt')
timeseries_dir = os.path.join(input_dir, 'timeseries_GLD_well')
output_file = os.path.join(input_dir, 'GLD_Well_ID_Location.csv')

# Read well IDs
with open(well_ids_file, 'r') as f:
    well_ids = [line.strip() for line in f.readlines()]

# Initialize list to store data
data = []

# Process each well
for well_id in well_ids:
    well_dir = os.path.join(timeseries_dir, well_id)
    txt_file = os.path.join(well_dir, f'gw_bro_{well_id}.txt')
    
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as f:
            lines = f.readlines()
            x = y = None
            for line in lines:
                if line.startswith('x :'):
                    x = float(line.split(':')[1].strip())
                if line.startswith('y :'):
                    y = float(line.split(':')[1].strip())
            if x is not None and y is not None:
                data.append([well_id, x, y])
    else:
        print(f"Metadata file not found for well {well_id}")

# Create DataFrame
df = pd.DataFrame(data, columns=['well_id', 'x', 'y'])

# Save DataFrame to CSV
df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")

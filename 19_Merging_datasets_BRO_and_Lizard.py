import os
import pickle
import pandas as pd

# Define the input and output paths
input_pklz_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/gw_bro_Netherlands.pklz'
output_base_directory = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/Lizard_dataset_gw_Netherlands/'

# Create the output base directory if it doesn't exist
if not os.path.exists(output_base_directory):
    os.makedirs(output_base_directory)

# Load the large dataset
with open(input_pklz_path, 'rb') as f:
    gw_bro = pickle.load(f)

# Print the column names to understand the structure of the DataFrame
print(f"Column names: {gw_bro.columns}")

# Check if 'monitoring_well' is in the columns
if 'monitoring_well' not in gw_bro.columns:
    raise KeyError("The column 'monitoring_well' does not exist in the dataset. Available columns are: " + ", ".join(gw_bro.columns))

# Function to sanitize well IDs
def sanitize_well_id(well_id):
    return well_id.replace("/", "_").replace("\\", "_")

# Iterate through the rows of the dataset to extract and save well data
for index, row in gw_bro.iterrows():
    try:
        well_id = sanitize_well_id(row['monitoring_well'])
        tube_nr = row['tube_nr']
        well_directory = os.path.join(output_base_directory, well_id, f"Tube_{tube_nr}")

        # Create a directory for the current tube within the well ID
        if not os.path.exists(well_directory):
            os.makedirs(well_directory)

        well_data = row.to_dict()

        # Ensure obs is a DataFrame and format it correctly
        time_series = well_data['obs']
        if isinstance(time_series, pd.DataFrame):
            time_series.reset_index(inplace=True)

            # Save the well data as a text file
            with open(os.path.join(well_directory, f'gw_bro_{well_id}_Tube_{tube_nr}.txt'), 'w') as f:
                f.write(f"screen_bottom: {well_data.get('screen_bottom')}\n")
                f.write(f"ground_level: {well_data.get('ground_level')}\n")
                f.write(f"tube_top: {well_data.get('tube_top')}\n")
                f.write(f"metadata_available: {well_data.get('metadata_available')}\n")
                f.write("\n-----time series------\n")
                f.write(time_series.to_string(index=False))

            # Save the well data as an Excel file
            time_series.to_excel(os.path.join(well_directory, f'gw_bro_{well_id}_Tube_{tube_nr}.xlsx'), index=False)

            # Save the well data as a pickle file
            with open(os.path.join(well_directory, f'gw_bro_{well_id}_Tube_{tube_nr}.pklz'), 'wb') as pkl_file:
                pickle.dump(well_data, pkl_file)

            print(f"Data for well ID {well_id} saved successfully.")

    except Exception as e:
        print(f"Failed to process well ID {well_id}: {e}")

import pandas as pd

# Load the first file
file_path_1 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/GLD_Well_ID_Location_with_dates.csv'
df1 = pd.read_csv(file_path_1)

# Load the second file
file_path_2 = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/timeseries_gw_Netherlands_hydropandas/Wells_data_Lizard_1958_2015_locations_missing_value.csv'
df2 = pd.read_csv(file_path_2)

# Reorder the columns in the second dataframe to match the first dataframe
df2 = df2[['well_id', 'x', 'y', 'time_range_start', 'time_range_end', 'screen_bottom', 'ground_level', 'screen_top', 'tube_top', 'missing_percentage']]

# Concatenate the two dataframes
combined_df = pd.concat([df1, df2], ignore_index=True)

# Save the combined dataframe to a new CSV file
output_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/input/Lizard_PDOK_all_data_wells_location_depth_missing_value_percentage.csv'
combined_df.to_csv(output_path, index=False)

# Print the total number of well_id's
total_well_ids = combined_df['well_id'].nunique()
print(f"Total number of well_id's: {total_well_ids}")

print(f"Data combined and saved to {output_path}")

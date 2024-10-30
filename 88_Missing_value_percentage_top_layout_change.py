import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Define file paths
# eerste plot: missing_data_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/tables/Observed_data/missing_data_percentages_top_timeseries.csv'
missing_data_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_output/missing_data_percentages_top_1980_2015.csv'
well_locations_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/tables/Model_GLOBGM/GLOBGM_Well_data_and_locations/well_locations_top_mapping.csv'
# shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/shapefiles/NL/Netherlands.shp' #oude shapefile
shapefile_path = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries_wgs84.shp'

# Load the missing data percentages
missing_data_df = pd.read_csv(missing_data_file)

# Extract the pixel number from the filename and convert to int
missing_data_df['pixel_id'] = missing_data_df['File'].str.extract(r'(\d+)').astype(int)

# Load the well locations
well_locations_df = pd.read_csv(well_locations_file)

# Extract the numeric part of well_id and convert to int
well_locations_df['well_id'] = well_locations_df['well_id'].str.extract(r'(\d+)').astype(int)

# Merge the missing data percentages with the well locations
merged_df = pd.merge(missing_data_df, well_locations_df, left_on='pixel_id', right_on='well_id', how='left')

# Create a GeoDataFrame from the merged data
gdf = gpd.GeoDataFrame(merged_df, geometry=gpd.points_from_xy(merged_df.lon, merged_df.lat), crs="EPSG:4326")

# Load the shapefile
nl_shapefile = gpd.read_file(shapefile_path)

# Define the colormap
#cmap = mcolors.LinearSegmentedColormap.from_list('mycmap', ['green', 'yellow', 'red'])
cmap = plt.get_cmap('seismic')  # or 'cividis'

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
nl_shapefile.plot(ax=ax, color='lightgrey', edgecolor='black')
gdf.plot(column='MissingDataPercentage', ax=ax, legend=False, cmap=cmap, markersize=75, marker='s')

plt.title('Percentage of Missing Data in Groundwater Levels \nper Pixel (1980-2015) for the Top Layer')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Adjust the color bar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=100))
sm._A = []
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Percentage of Missing Data %')

plt.show()

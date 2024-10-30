import pandas as pd
import geopandas as gpd

# Path naar je GeoPackage bestand
gpkg_path = '/Users/tomdeboer/Downloads/brogldvolledigeset.gpkg'

# Lees het GeoPackage bestand
gdf = gpd.read_file(gpkg_path)

# Stel de weergave-opties in om alle kolommen te tonen
pd.set_option('display.max_columns', None)

# Tel het aantal rijen
row_count = len(gdf)

# Verkrijg de kolomnamen
column_names = gdf.columns.tolist()

# Bekijk de eerste paar rijen van de dataset
first_rows = gdf.head()

print(f"Het GeoPackage-bestand bevat {row_count} rijen.")
print("Kolomnamen zijn:", column_names)
print("Eerste paar rijen van de dataset:")
print(first_rows)



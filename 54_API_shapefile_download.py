import requests
import geopandas as gpd

# GeoJSON URL
geojson_url = 'https://service.pdok.nl/cbs/gebiedsindelingen/2021/wfs/v1_0?request=GetFeature&service=WFS&version=1.1.0&outputFormat=application%2Fjson&typeName=gebiedsindelingen:provincie_gegeneraliseerd'

# File path to save the GeoJSON locally
geojson_file = '/Users/tomdeboer/Documents/geojson_provinces.json'

# Download the GeoJSON data using requests
response = requests.get(geojson_url)

if response.status_code == 200:
    with open(geojson_file, 'w') as file:
        file.write(response.text)
    print("GeoJSON file downloaded successfully.")
else:
    print(f"Failed to download GeoJSON. Status code: {response.status_code}")

# Load the saved GeoJSON file using GeoPandas
gdf = gpd.read_file(geojson_file)

# Save it as a Shapefile
gdf.to_file('/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/controle/controle_input/shp_provinces/province_boundaries.shp', driver='ESRI Shapefile')

print("Shapefile saved successfully.")
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
# Zorg ervoor dat je seaborn hebt geïnstalleerd
# pip install seaborn

outputDirectory = '../../input/timeseries_gw_Netherlands_hydropandas/'

# Laad het pklz-bestand
pklz_filepath = os.path.join(outputDirectory, 'gw_bro_Netherlands.pklz')
with open(pklz_filepath, 'rb') as f:
    gw_bro = pickle.load(f)

# Controleer of het een DataFrame is en converteer zo nodig
if isinstance(gw_bro, pd.DataFrame):
    df = gw_bro
else:
    raise ValueError("Onbekend type object in het pklz-bestand")

# Zorg ervoor dat de datums correct zijn
df['date'] = pd.to_datetime(df['date'])

# Bereken maandelijkse en jaarlijkse gemiddelden
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.to_period('M')

# Groeperen en gemiddelden berekenen
monthly_means = df.groupby('month')['value'].mean().reset_index()
yearly_means = df.groupby('year')['value'].mean().reset_index()

# Plotten van de maandelijkse gemiddelden
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_means, x='month', y='value')
plt.title('Gemiddelde Waarden per Maand')
plt.xlabel('Maand')
plt.ylabel('Gemiddelde Waarde')
plt.xticks(rotation=45)
plt.show()

# Plotten van de jaarlijkse gemiddelden
plt.figure(figsize=(12, 6))
sns.lineplot(data=yearly_means, x='year', y='value')
plt.title('Gemiddelde Waarden per Jaar')
plt.xlabel('Jaar')
plt.ylabel('Gemiddelde Waarde')
plt.xticks(rotation=45)
plt.show()

# Opslaan van de gemiddelden naar CSV
monthly_means.to_csv(os.path.join(outputDirectory, 'monthly_means.csv'), index=False)
yearly_means.to_csv(os.path.join(outputDirectory, 'yearly_means.csv'), index=False)

# Gemiddelde waarden kaart maken (vereist coördinaten)


# Zorg ervoor dat er coördinaten zijn
if 'x' in df.columns and 'y' in df.columns:
    # Groeperen op locatie en gemiddelde berekenen
    location_means = df.groupby(['x', 'y'])['value'].mean().reset_index()

    # Maak een GeoDataFrame
    gdf = gpd.GeoDataFrame(location_means, geometry=gpd.points_from_xy(location_means.x, location_means.y))

    # Plotten van de kaart
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    gdf.plot(column='value', ax=ax, legend=True, cmap='coolwarm', markersize=5)
    plt.title('Gemiddelde Waarden per Locatie')
    plt.show()
else:
    print("Geen coördinaten gevonden in de data. Kaart kan niet worden gemaakt.")


import os
import hydropandas as hpd
import pickle
import pandas as pd

outputDirectory = '../../input/timeseries_gw_Netherlands_hydropandas/'

# Zorg ervoor dat het output directory bestaat
if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

# Bestandspad van het pklz bestand
pklz_filepath = os.path.join(outputDirectory, 'gw_bro_Netherlands.pklz')

# Laad het pklz bestand
with open(pklz_filepath, 'rb') as f:
    obj = pickle.load(f)

# Controleer het type van het object om te zien hoe we de kolomnamen kunnen extraheren
if isinstance(obj, pd.DataFrame):
    # Als het een DataFrame is, gebruik het direct
    df = obj
    print("Kolommen in DataFrame:")
    print(df.columns)
elif isinstance(obj, hpd.GroundwaterObsCollection):
    # Als het een GroundwaterObsCollection is, converteer het naar een DataFrame
    df = obj.to_dataframe()
    print("Kolommen in GroundwaterObsCollection DataFrame:")
    print(df.columns)
else:
    print("Onbekend type object:", type(obj))
    df = None

# Eventueel: Schrijf de kolomnamen naar een tekstbestand
if df is not None:
    with open(os.path.join(outputDirectory, 'gw_bro_Netherlands_columns.txt'), 'w') as f:
        for column in df.columns:
            f.write(f"{column}\n")
    print("Kolommen zijn geschreven naar gw_bro_Netherlands_columns.txt")
else:
    print("Kon geen kolomnamen schrijven vanwege onbekend objecttype")


# Als het een DataFrame is, print de details
if df is not None:
    print("Kolommen in DataFrame:")
    print(df.columns)
    print("\nAantal rijen:", len(df))
    print("\nEerste 10 rijen:")
    print(df.head(10))
else:
    print("Kon geen details weergeven vanwege onbekend objecttype")
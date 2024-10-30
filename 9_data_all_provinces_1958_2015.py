import os
import requests
import hydropandas as hpd
import pickle
import pprint
import time
from requests.exceptions import ConnectionError, JSONDecodeError, RequestException

outputDirectory = '../../input/timeseries_gw_Provinces_Netherlands_hydropandas/'

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

# Define the extents for each province in Rijksdriehoekscoördinaten (example values)
provinces_extents = {
    'Groningen': (210000, 276880, 540000, 617911),
    'Friesland': (152592, 224682, 182151, 615346),
    'Drenthe': (204170, 270000, 514296, 580000),
    'Overijssel': (185282, 270102, 459640, 522920),
    'Flevoland': (136893, 195455, 473867, 539797),
    'Gelderland': (126333, 254343, 415935, 472935),
    'Utrecht': (114499, 171562, 430059, 479599),
    'Noord-Holland': (94088, 149318, 463851, 577689),
    'Zuid-Holland': (47995, 130474, 406278, 482634),
    'Zeeland': (13474, 77768, 357571, 420160),
    'Noord-Brabant': (72039, 200800, 359029, 426903),
    'Limburg': (167385, 213783, 307000, 398267),
}

# Placeholder for the correct BRO API URL
# Make sure to replace this with the actual API endpoint URL
bro_api_url = " Fill in with correct link!! "  # Example URL

max_retries = 5
retry_delay = 5  # seconds

for province, extent in provinces_extents.items():
    for attempt in range(max_retries):
        try:
            # Debugging output to check extent and attempt
            print(f"Attempting to download data for {province} with extent {extent} (Attempt {attempt + 1})")
            
            # Prepare the payload
            payload = {
                "extent": {
                    "xmin": extent[0],
                    "xmax": extent[1],
                    "ymin": extent[2],
                    "ymax": extent[3]
                }
            }
            
            # Headers for the request (add any required headers, such as authentication tokens)
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Replace with your actual access token if needed
            }

            # Make the request to the BRO API
            response = requests.post(bro_api_url, json=payload, headers=headers)

            # Check the status code of the response
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                print("Successful response:", json.dumps(data, indent=4))
                break
            else:
                print(f"Error: Received status code {response.status_code}")
                print("Response text:", response.text)

        except ConnectionError as e:
            print(f"Attempt {attempt + 1} failed for {province}: {e}. Connection error. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except JSONDecodeError as e:
            print(f"Attempt {attempt + 1} failed for {province}: JSON decode error: {e}.")
            time.sleep(retry_delay)
        except RequestException as e:
            print(f"An unexpected error occurred for {province} on attempt {attempt + 1}: {e}")
            time.sleep(retry_delay)
    else:
        raise Exception(f"Max retries exceeded for {province}. Could not fetch data.")

    # Save the data for each province (assuming 'data' is the correct variable)
    province_output_path = os.path.join(outputDirectory, f'gw_bro_{province}.pklz')
    with open(province_output_path, 'wb') as f:
        pickle.dump(data, f)
    print(f"Data for {province} saved to {province_output_path}")

    with open(os.path.join(outputDirectory, f'gw_bro_{province}.txt'), "a") as f:
        pprint.pprint(data, stream=f)

    # Assuming 'data' can be converted to a DataFrame for saving as Excel
    # Replace with correct conversion if needed
    import pandas as pd
    df = pd.DataFrame(data)  # Adjust this based on the actual structure of 'data'
    df.to_excel(os.path.join(outputDirectory, f'gw_bro_{province}.xlsx'))

print("All data downloaded and saved successfully.")

import requests
import pandas as pd
try:
    animals_api = requests.get('http://127.0.0.1:8000/all/animals')
    animals_api.raise_for_status()  
    animals_api_data = animals_api.json()

    guiders_api = requests.get('http://127.0.0.1:8000/all/guiders')
    guiders_api.raise_for_status()  
    guiders_api_data = guiders_api.json()
    adf = pd.DataFrame(animals_api_data)
    gdf = pd.DataFrame(guiders_api_data)
    # print(adf)
    # print(gdf)
    inner_merged_df = pd.merge(adf, gdf, on='id', how='inner')
    print(adf.dtypes)
    # print(inner_merged_df.head())
    # print(inner_merged_df.isnull().sum())
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
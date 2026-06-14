import requests
import pandas as pd

# 1. Define query parameters (Example: Atacama Desert, Chile)
lat = -23.8634
lon = -69.1328
start_date = "20160101" # Format YYYYMMDD (Last 10 years)
end_date = "20251231"

# Variables requested from NASA:
# ALLSKY_SFC_SW_DWN = Global Horizontal Irradiance (GHI)
# T2M = Temperature at 2 meters
url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN,T2M&community=RE&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"

print("Connecting to NASA POWER API...")
response = requests.get(url)

# 2. Validate successful connection (HTTP Status 200 means "OK")
if response.status_code == 200:
    data = response.json()
    
    # 3. Extract the data section from the nested JSON
    # NASA provides data inside 'properties' -> 'parameter'
    dict_ghi = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
    dict_temp = data['properties']['parameter']['T2M']
    
    # Convert dictionaries to Pandas DataFrames
    df_ghi = pd.DataFrame(list(dict_ghi.items()), columns=['date', 'ghi_kwh_m2'])
    df_temp = pd.DataFrame(list(dict_temp.items()), columns=['date', 'temperature_c'])
    
    # Merge both DataFrames using the date as key
    df_final = pd.merge(df_ghi, df_temp, on='date')
    
    # 4. Enrich the DataFrame with coordinates for the database
    df_final['latitude'] = lat
    df_final['longitude'] = lon
    
    # Reorder columns to match the PostgreSQL schema
    df_final = df_final[['date', 'latitude', 'longitude', 'ghi_kwh_m2', 'temperature_c']]
    
    # 5. Data Cleaning
    # NASA uses -999.0 for missing satellite data; replace with standard missing value
    df_final = df_final.replace(-999.0, pd.NA)
    
    # Transform the 'YYYYMMDD' text column to a datetime format
    df_final['date'] = pd.to_datetime(df_final['date'], format='%Y%m%d')
    
    print("\nData successfully extracted and processed!")
    print("-" * 50)
    print(df_final.head()) # Show the first 5 rows to verify
    print("-" * 50)
    print(f"Total records retrieved: {len(df_final)} days.")

else:
    print(f"Connection error. Status code: {response.status_code}")
    print(response.text)
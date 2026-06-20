import requests
import pandas as pd
import numpy as np

def extract_nasa(lat, lon, start_date, end_date):
    """
    Extracts and cleans historical radiation and temperature data from NASA POWER API.
    """
    print(f"Connecting to NASA API for coordinates ({lat}, {lon})...")
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN,T2M&community=RE&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        dict_ghi = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        dict_temp = data['properties']['parameter']['T2M']
        
        #asdasd

        df_ghi = pd.DataFrame(list(dict_ghi.items()), columns=['date', 'ghi_kwh_m2'])
        df_temp = pd.DataFrame(list(dict_temp.items()), columns=['date', 'temperature_c'])
        
        df_final = pd.merge(df_ghi, df_temp, on='date')
        df_final['latitude'] = lat
        df_final['longitude'] = lon
        df_final = df_final[['date', 'latitude', 'longitude', 'ghi_kwh_m2', 'temperature_c']]
        
        # Data Cleaning
        df_final = df_final.replace(-999.0, np.nan)
        df_final['date'] = pd.to_datetime(df_final['date'], format='%Y%m%d')
        
        print(f"Successfully extracted {len(df_final)} records.")
        return df_final 
    else:
        print(f"Connection error. Status code: {response.status_code}")
        return None
    

# --- DIRECT CALL ---
if __name__ == '__main__':
    df_resultado = extract_nasa(-23.8634, -69.1328, "20160101", "20251231")
    
    # Sucessful extraction, first rows will be showed
    if df_resultado is not None:
        print("\nPreview of extracted data:")
        print(df_resultado.head())
# Archivo: hourly_weather.py
import pandas as pd
import time
import datetime
from extract_weather import extract_current_weather
from load import load_to_postgres
from load_sheets import load_to_google_sheets
from chile_provinces import CHILE_PROVINCES  # Importación del mapa completo

if __name__ == "__main__":

    print(f"\n==================================================")
    print(f"BEGINNING NATIONAL PIPELINE (CHILE): {datetime.datetime.now()}")
    print(f"==================================================")
    
    list_dataframes = []
    total_provinces = len(CHILE_PROVINCES)
    
    # Loop to use API province by province
    for i, item in enumerate(CHILE_PROVINCES, 1):
        prov = item["province"]
        reg = item["region"]
        print(f"[{i}/{total_provinces}] Procesando: {prov} -> Región: {reg}...")
        
        # Dynamic call to API
        df_prov = extract_current_weather(item["lat"], item["lon"])
        
        if df_prov is not None:
            # Stamp labels
            df_prov["province"] = prov
            df_prov["region"] = reg
            list_dataframes.append(df_prov)
            
        # Flow control: pause 1 second to avoid blockages on API
        time.sleep(1)

    
    columns_order = [
        "datetime", 
        "latitude", 
        "longitude", 
        "region", 
        "province", 
        "cloudiness_pct", 
        "temperature_current"
    ]
        
    # If data is extracted
    if list_dataframes:

        print("\nConsolidating the national data matrix...")
        df_national = pd.concat(list_dataframes, ignore_index=True)

        # 1. LOCAL UPLOAD
        load_to_postgres(df_national[columns_order], "current_weather")
        
        # 2. CLOUD UPLOAD
        load_to_google_sheets(df_national[columns_order], "SolarTech_Data")
        
        print(f"\n==================================================")
        print(f"✅ SUCESS: Data procesed and inserted into {len(df_national)} provincias.")
        print(f"==================================================")
    else:
        print("\n❌ ERROR: Provinces information couldn't be obtained.")
        
    print(f"--- Pipeline ended sucesfuly at{datetime.datetime.now()} ---\n")
import os
import urllib.parse  # Protects your connection from special character crashes
import pandas as pd
import requests
import time
import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
from chile_provinces import CHILE_PROVINCES

# Load local environment variables from your .env file
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS") 
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# CRITICAL FIX: URL-encode credentials to safely handle characters like 'ó' or 'ñ' from your .env
SAFE_USER = urllib.parse.quote_plus(DB_USER) if DB_USER else "postgres"
SAFE_PASS = urllib.parse.quote_plus(DB_PASS) if DB_PASS else ""

# Construct the secure connection URI string using encoded values
DB_URI = f"postgresql://{SAFE_USER}:{SAFE_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def fetch_nasa_historical_data(lat, lon, start_date="20160101", end_date="20251231"):
    """
    Connects to the NASA POWER API to fetch daily global horizontal irradiance (GHI)
    and temperature for specific geographic coordinates over a 10-year period.
    """
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            ghi_dict = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
            temp_dict = data["properties"]["parameter"]["T2M"]
            
            df = pd.DataFrame({
                "date_str": ghi_dict.keys(),
                "ghi_kwh_m2": ghi_dict.values(),
                "temperature_c": temp_dict.values()
            })

            # Parse date format to a native Pandas Datetime Timestamp for clean SQL injection
            df["date"] = pd.to_datetime(df["date_str"], format="%Y%m%d")
            df.drop(columns=["date_str"], inplace=True)
            
            return df
        else:
            print(f"❌ NASA API Error: Status Code {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Connection Error with NASA API: {e}")
        return None

if __name__ == "__main__":
    print(f"\n==================================================")
    print(f"STARTING NATIONAL HISTORICAL PIPELINE: {datetime.datetime.now()}")
    print(f"==================================================")
    
    # Initialize SQLAlchemy database engine safely
    engine = create_engine(DB_URI)
    total_provinces = len(CHILE_PROVINCES)
    
    # Loop iteratively through all 56 Chilean provinces
    for index, item in enumerate(CHILE_PROVINCES, 1):
        prov = item["province"]
        reg = item["region"]
        lat = item["lat"]
        lon = item["lon"]
        
        print(f"[{index}/{total_provinces}] Fetching 10-Year NASA Data for: {prov} ({reg})...")
        
        # Extract data from NASA POWER API
        df_history = fetch_nasa_historical_data(lat, lon)
        
        if df_history is not None and not df_history.empty:
            # Map structural geographic metadata to the DataFrame
            df_history["latitude"] = round(float(lat), 6)
            df_history["longitude"] = round(float(lon), 6)
            df_history["region"] = str(reg)
            df_history["province"] = str(prov)
            
            # Ensure correct data alignment matching the PostgreSQL schema
            df_history = df_history[[
                "date", "latitude", "longitude", "region", 
                "province", "ghi_kwh_m2", "temperature_c"
            ]]
            
            try:
                # Append data chunk directly to PostgreSQL table
                df_history.to_sql("historic_radiation", engine, if_exists="append", index=False)
                print(f"   Successfully loaded {len(df_history)} daily records to database.")
            except Exception as database_error:
                print(f"\n❌ !!! DATABASE CONNECTION OR SCHEMA CRASH ON PROVINCE: {prov} !!!")
                print(f"Error Type: {type(database_error).__name__}")
                print(f"Error Details: {str(database_error)}")
                print(f"==================================================\n")
                break  # Interrupt loop immediately so you can read the error message clearly
        else:
            print(f"   ⚠️ Warning: Empty dataset returned for {prov}.")
        
        # API Rate Limit Safety window
        time.sleep(1.5)
        
    print(f"\n==================================================")
    print(f"✅ PIPELINE PROCESS ATTEMPT FINISHED AT {datetime.datetime.now()}")
    print(f"==================================================")
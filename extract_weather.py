import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def extract_current_weather(lat, lon):
    """
    Extracts real-time weather data (temperature and cloudiness) from OpenWeatherMap API.
    """
    print(f"Connecting to OpenWeatherMap API for coordinates ({lat}, {lon})...")
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: OPENWEATHER_API_KEY not found in environment variables.")
        return None
        
    # URL for current weather data
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Parse the nested JSON response into a structured dictionary
        weather_data = {
            # Convert current system time to UTC timestamp with time zone
            'datetime': pd.to_datetime('now', utc=True),
            # Match your exact pgAdmin column names layout
            'latitude': lat,
            'longitude': lon,
            'cloudiness_pct': data['clouds']['all'],
            'temperature_current': data['main']['temp']
        }
        
        # Convert to DataFrame
        df_weather = pd.DataFrame([weather_data])
        print("Successfully extracted current weather data.")
        return df_weather
    else:
        print(f"Connection error to OpenWeather. Status code: {response.status_code}")
        print(response.text)
        return None
    
# --- DIRECT EXECUTION ---
if __name__ == '__main__':
    # Test Coordinates (Atacama Desert)
    lat_prueba = -23.8634
    lon_prueba = -69.1328
    
    # Function calling
    df_resultado = extract_current_weather(lat_prueba, lon_prueba)
    
    # If extraction is succesful we show the datas
    if df_resultado is not None:
        print("\nPreview of the current weather data:")
        print(df_resultado)
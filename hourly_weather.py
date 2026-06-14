from extract_weather import extract_current_weather
from load import load_to_postgres
import datetime

if __name__ == "__main__":
    print(f"\n--- Ejecutando extracción automática: {datetime.datetime.now()} ---")
    
    # Atacama Desert
    lat = -23.8634
    lon = -69.1328
    
    df_current = extract_current_weather(lat, lon)
    
    if df_current is not None:
        load_to_postgres(df_current, "current_weather")
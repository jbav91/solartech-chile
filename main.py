from extraction_nasa import extract_nasa
from extract_weather import extract_current_weather
from load import load_to_postgres

if __name__ == "__main__":
    print("--- Starting ETL Pipeline ---")

    # Target Coordinates: Atacama Desert, Chile
    target_lat = -23.8634
    target_lon = -69.1328
    
    # 1. RUN HISTORICAL PIPELINE (NASA POWER)
    print("\n--- Phase 1: Historical Data Extraction ---")
    df_historic = extract_nasa(target_lat, target_lon, "20160101", "20251231")
    if df_historic is not None:
        load_to_postgres(df_historic, "historic_radiation")
        
    # 2. RUN REAL-TIME PIPELINE (OPENWEATHERMAP)
    print("\n--- Phase 2: Real-Time Weather Extraction ---")
    df_current = extract_current_weather(target_lat, target_lon)
    if df_current is not None:
        load_to_postgres(df_current, "current_weather")

        
    print("--- ETL Pipeline Finished ---")
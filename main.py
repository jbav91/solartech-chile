from extraction_nasa import extract_nasa
from load import load_to_postgres

if __name__ == "__main__":
    print("--- Starting ETL Pipeline ---")
    
    # 1. Extract (E) & Transform (T)
    datos = extract_nasa(-23.8634, -69.1328, "20160101", "20251231")
    
    # 2. Load (L)
    if datos is not None:
        load_to_postgres(datos, "historic_radiation")
        
    print("--- ETL Pipeline Finished ---")
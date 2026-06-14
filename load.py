# Archivo: load.py
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def load_to_postgres(df, table_name):
    """
    Loads a Pandas DataFrame into a PostgreSQL database securely.
    """
    # Leer credenciales desde el entorno virtual (ocultas)
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    print(f"\nConnecting to PostgreSQL to load data into '{table_name}'...")
    
    try:
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print("Success: Data successfully loaded into PostgreSQL!")
        
    except Exception as e:
        print(f"Database Connection Error: {e}")
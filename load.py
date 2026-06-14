import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# .env varibles
load_dotenv()

def load_to_postgres(df, table_name):
    """
    Loads a Pandas DataFrame into a PostgreSQL database securely.
    """
    # Read credentials from .env
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    print(f"\nConnecting to PostgreSQL to load data into '{table_name}'...")
    
    try:
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        # Ensure missing values are properly converted to SQL NULL
        df = df.replace({float('nan'): None})
        
        # Send data to SQL
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print("Success: Data successfully loaded into PostgreSQL!")
        
    except Exception as e:
        print(f"Database Connection Error: {e}")
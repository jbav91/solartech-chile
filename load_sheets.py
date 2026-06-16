import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def load_to_google_sheets(df, spreadsheet_name):
    """
    Connects with Google sheets using Service Account and adds Dataframe data.
    """
    print(f"Connectins to Google Sheets for updating '{spreadsheet_name}'...")
    
    # Security Scopes for Google Drive and Google Sheets
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        # Autentication with JSON file
        creds = ServiceAccountCredentials.from_json_keyfile_name('solartech-chile-credentials.json', scopes)
        client = gspread.authorize(creds)
        
        # Open the Google Sheets by it name
        spreadsheet = client.open(spreadsheet_name)
        sheet = spreadsheet.sheet1  # Selects the first tab.
        
        # Format dates into text to avoid conflicts
        df_clean = df.copy()
        for col in df_clean.columns:
            if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                # Convert into a string directly, keeping ISO format with Timezone (+00:00)
                df_clean[col] = df_clean[col].astype(str)
        
        # If the sheet is empty, Headers will be written
        valores_actuales = sheet.get_all_values()
        if len(valores_actuales) == 0:
            sheet.append_row(df_clean.columns.tolist())
            
        # Insert new rows at the ned of the sheet
        for _, row in df_clean.iterrows():
            sheet.append_row(row.tolist())
            
        print("Success: Data uploaded into Google Sheet!")
        
    except Exception as e:
        print(f"Error: Connection with Google Sheets: {e}")
@echo off
echo Initiating SolarTech ETL process...

:: 1. Go to the exact folder of the project
cd "C:\Users\jbav9\OneDrive\Desktop\Portafolio\Data Analyst\SolarTech Chile\Code"

:: 2. Execute the script and save everythign on a text file
python hourly_weather.py >> record_etl.txt 2>&1
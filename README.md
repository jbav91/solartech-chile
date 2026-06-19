# ☀️ SolarTech Chile: End-to-End Solar PV Calculator & Geographic Dashboard

[![Tableau Public](https://img.shields.io/badge/Tableau-Live_Dashboard-E97627?style=for-the-badge&logo=Tableau)](tu-enlace-de-tableau-aqui)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)]()

## 📌 Project Overview
**SolarTech Chile** is an end-to-end data pipeline and interactive business intelligence tool designed for the Chilean renewable energy market. It bridges the gap between raw meteorological data and real-world business applications, allowing users to accurately estimate their solar panel requirements and financial investment based on historical geographic radiation, energy consumption, and specific hardware choices.

This project demonstrates a full-stack data workflow: from API data extraction and relational database architecture to complex mathematical modeling and advanced UX/UI dashboard design.

## ⚙️ Tech Stack & Tools
* **Data Extraction & Transformation:** Python, `requests`, `pandas`
* **External APIs:** NASA POWER API (Historical Climate Data)
* **Database Architecture:** PostgreSQL
* **Data Visualization & BI:** Tableau Desktop / Tableau Public

## 🏗️ Architecture & Data Pipeline

### 1. Data Engineering (Python)
* Engineered a Python script to programmatically query the **NASA POWER API**, extracting historical solar radiation and temperature data across Chile (2016-2025).
* Utilized `pandas` to clean, transform, and structure the raw JSON/CSV responses, ensuring precise geographic granularity down to the regional and provincial levels.

### 2. Data Storage & Modeling (PostgreSQL)
* Architected a relational database to serve as the single source of truth.
* Created structured tables to separate massive historical weather data (`historic_radiation`) from the hardware catalog (`pv_panels`), ensuring scalable and normalized data management.

### 3. Business Intelligence & Analytics (Tableau)
* **Dynamic Translation:** Built functional parameters and `CASE` statements to inject specific technical specifications (Wattage) and financial data (Pricing) into the dashboard's memory based on user hardware selection.
* **Mathematical Modeling:** Engineered complex calculated fields to determine exact panel requirements. The formula cross-references consumption, panel capacity, 75% system efficiency, and localized average solar radiation `AVG(Ghi Kwh M2)`.
* **Advanced UX/UI:** 
  * Replaced standard dropdowns with interactive, shape-based visual selectors.
  * Configured targeted Dashboard Actions for a seamless, real-time calculation experience.
  * Designed smart, context-aware titles using logical operators and the `COUNTD()` function.
  * Created a custom **Mobile-First Layout** using Device Designer for cross-device accessibility.

## 🗂️ Repository Structure
```text
├── data/                   # Sample datasets (CSV/JSON) used for testing
├── scripts/                # Python scripts for NASA POWER API extraction and ETL
├── sql/                    # SQL scripts for PostgreSQL table creation and data loading
├── tableau/                # Tableau workbook file (.twb / .twbx)
└── README.md               # Project documentation

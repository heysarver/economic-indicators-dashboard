import requests
import pandas as pd
from datetime import datetime, timedelta
import logging
import os

logging.basicConfig(level=logging.INFO)

def fetch_fred_data(series_id, start_date, end_date):
    api_key = os.environ.get('FRED_API_KEY')
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    
    logging.info(f"Fetching FRED data for series {series_id}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['observations']
        logging.info(f"Successfully fetched {len(data)} records for FRED series {series_id}")
        return pd.DataFrame(data)
    else:
        logging.error(f"Failed to fetch FRED data: {response.status_code}")
        logging.error(f"Response content: {response.text}")
        raise Exception(f"Failed to fetch FRED data: {response.status_code}. Response: {response.text}")

def fetch_all_data():
    logging.info("Starting to fetch all data")
    current_year = datetime.now().year
    start_year = current_year - 50
    start_date = f"{start_year}-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")

    # Fetch CPI data from FRED
    cpi_data = fetch_fred_data("CPIAUCSL", start_date, end_date)
    
    # Fetch Treasury rates data from FRED
    fed_2y = fetch_fred_data("DGS2", start_date, end_date)
    fed_5y = fetch_fred_data("DGS5", start_date, end_date)
    fed_10y = fetch_fred_data("DGS10", start_date, end_date)
    fed_30y = fetch_fred_data("DGS30", start_date, end_date)

    # Fetch PPI data from FRED
    ppi_data = fetch_fred_data("PPIACO", start_date, end_date)

    # Fetch Unemployment Rate data from FRED
    unemployment_data = fetch_fred_data("UNRATE", start_date, end_date)

    # Fetch Retail Sales: Food Services data from FRED (as a proxy for farm income)
    farm_income_data = fetch_fred_data("RSAFS", start_date, end_date)

    # Fetch US GDP data from FRED
    gdp_data = fetch_fred_data("GDP", start_date, end_date)

    # Fetch Industrial Production Index data from FRED
    industrial_production_data = fetch_fred_data("INDPRO", start_date, end_date)

    # Fetch Retail Sales data from FRED
    retail_sales_data = fetch_fred_data("RSAFS", start_date, end_date)

    # Fetch Housing Starts data from FRED
    housing_starts_data = fetch_fred_data("HOUST", start_date, end_date)

    logging.info("Finished fetching all data")
    return {
        'cpi': cpi_data,
        'fed_2y': fed_2y,
        'fed_5y': fed_5y,
        'fed_10y': fed_10y,
        'fed_30y': fed_30y,
        'ppi': ppi_data,
        'unemployment': unemployment_data,
        'farm_income': farm_income_data,
        'gdp': gdp_data,
        'industrial_production': industrial_production_data,
        'retail_sales': retail_sales_data,
        'housing_starts': housing_starts_data
    }

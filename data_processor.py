import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def process_fred_data(data, calculate_pct_change=False):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna()
    df = df.sort_values('date')
    
    if calculate_pct_change:
        df['pct_change'] = (df['value'] / df['value'].shift(12) - 1) * 100  # Year-over-year percentage change
        
        # Log PPI value for March 2022
        march_2022 = df[df['date'] == '2022-03-01']
        if not march_2022.empty:
            logging.info(f"PPI value for March 2022: {march_2022['pct_change'].values[0]:.2f}%")
        else:
            logging.info("March 2022 data not found in PPI dataset")
        
        return df[['date', 'pct_change']].rename(columns={'pct_change': 'value'})
    
    return df[['date', 'value']]

def process_data(raw_data):
    processed_data = {}
    
    for key, data in raw_data.items():
        if key in ['cpi', 'ppi']:
            processed_data[key] = process_fred_data(data, calculate_pct_change=True)
        else:
            processed_data[key] = process_fred_data(data)
    
    return processed_data

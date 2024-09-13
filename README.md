# Economic Indicator Dashboard

This Streamlit app visualizes key economic indicators including the Consumer Price Index (CPI) and various Treasury Rates over the last 50 years.

## Features

- Interactive dashboard with two main tabs: CPI and Treasury Rates
- Date range selector to filter data
- Detailed graphs for CPI and 2-Year, 5-Year, 10-Year, and 30-Year Treasury Rates
- Brief descriptions of each economic indicator
- Data sourced from Federal Reserve Economic Data (FRED)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/economic-indicator-dashboard.git
   cd economic-indicator-dashboard
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Important: FRED API Key

This application requires a FRED API key to fetch economic data. Follow these steps to set up your API key:

1. Go to https://fred.stlouisfed.org/docs/api/api_key.html to get your API key
2. Set your API key as an environment variable:
   ```
   export FRED_API_KEY='your_api_key_here'
   ```
3. If you're using a .env file, add the following line:
   ```
   FRED_API_KEY=your_api_key_here
   ```

The application will not work without a valid FRED API key.

## Running the App

To run the app locally, use the following command:

```
streamlit run main.py
```

The app will open in your default web browser.

## Usage

1. Use the date range selector at the top of the page to filter the data for a specific time period.
2. Navigate between the CPI and Treasury Rates tabs to view different economic indicators.
3. Hover over the graphs to see specific data points.
4. Use the range slider below each graph to zoom in on specific time periods.

## Contributing

Contributions to improve the dashboard are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

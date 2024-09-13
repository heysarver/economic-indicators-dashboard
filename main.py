import streamlit as st
import pandas as pd
from data_fetcher import fetch_all_data
from data_processor import process_data
from visualizer import create_line_graph
from datetime import datetime, timedelta
import os
import base64
import io

st.set_page_config(page_title="Economic Indicator Dashboard", layout="wide")

# Update CSS for download buttons
st.markdown('''
<style>
.download-button {
    background-color: var(--primary-color);
    color: white;
    padding: 0.25rem 0.75rem;
    text-decoration: none;
    border-radius: 0.25rem;
    border: none;
    font-size: 0.875rem;
    transition: background-color 0.2s ease-in-out;
    display: inline-block;
    margin-top: 0.5rem;
    margin-right: 0.5rem;
}
.download-button:hover {
    background-color: var(--primary-color);
    filter: brightness(90%);
    color: white;
}
</style>
''', unsafe_allow_html=True)

def get_download_links(df, filename):
    csv = df.to_csv(index=False)
    b64_csv = base64.b64encode(csv.encode()).decode()
    href_csv = f'<a href="data:file/csv;base64,{b64_csv}" download="{filename}.csv" class="download-button">Download CSV</a>'
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    b64_excel = base64.b64encode(output.getvalue()).decode()
    href_excel = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="{filename}.xlsx" class="download-button">Download Excel</a>'
    
    return f"{href_csv} {href_excel}"

def main():
    st.title("Economic Indicator Dashboard")
    st.write("Visualizing key economic indicators over the last 50 years")

    if 'FRED_API_KEY' not in os.environ:
        st.error("FRED API key not found. Please set the FRED_API_KEY environment variable.")
        return

    try:
        # Fetch and process data
        raw_data = fetch_all_data()
        processed_data = process_data(raw_data)

        # Date range selector
        min_date = min(df['date'].min() for df in processed_data.values())
        max_date = max(df['date'].max() for df in processed_data.values())
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
        with col2:
            end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

        # Filter data based on selected date range
        for key in processed_data:
            processed_data[key] = processed_data[key][(processed_data[key]['date'] >= pd.Timestamp(start_date)) & 
                                                      (processed_data[key]['date'] <= pd.Timestamp(end_date))]

        # Create tabs for different indicators
        tabs = st.tabs(["Price Indices", "Treasury Rates", "Unemployment", "Farm Income", "GDP", "Other Indicators", "Comparison"])

        with tabs[0]:
            st.header("Price Indices")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Consumer Price Index (CPI)")
                st.write("""
                The Consumer Price Index (CPI) measures the average change over time in the prices paid by urban consumers for a market basket of consumer goods and services.
                It is a key indicator of inflation in the economy.
                """)
                st.markdown(get_download_links(processed_data['cpi'], 'cpi_data'), unsafe_allow_html=True)
                fig_cpi = create_line_graph(processed_data['cpi'], 'Consumer Price Index (CPI) - Year-over-Year Change', 'Percentage Change (%)', is_percentage=True)
                st.plotly_chart(fig_cpi, use_container_width=True)

            with col2:
                st.subheader("Producer Price Index (PPI)")
                st.write("""
                The Producer Price Index (PPI) measures the average change over time in the selling prices received by domestic producers for their output.
                It is an indicator of inflation in the production process.
                """)
                st.markdown(get_download_links(processed_data['ppi'], 'ppi_data'), unsafe_allow_html=True)
                fig_ppi = create_line_graph(processed_data['ppi'], 'Producer Price Index (PPI) - Year-over-Year Change', 'Percentage Change (%)', is_percentage=True)
                st.plotly_chart(fig_ppi, use_container_width=True)

        with tabs[1]:
            st.header("Treasury Rates")
            st.write("""
            Treasury rates are the interest rates that the U.S. government pays to borrow money for different lengths of time.
            These rates serve as a benchmark for other interest rates in the economy and are considered risk-free rates.
            """)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(get_download_links(processed_data['fed_2y'], '2y_treasury_rate'), unsafe_allow_html=True)
                fig_2y = create_line_graph(processed_data['fed_2y'], '2-Year Treasury Rate', 'Interest Rate (%)')
                st.plotly_chart(fig_2y, use_container_width=True)
                
                st.markdown(get_download_links(processed_data['fed_10y'], '10y_treasury_rate'), unsafe_allow_html=True)
                fig_10y = create_line_graph(processed_data['fed_10y'], '10-Year Treasury Rate', 'Interest Rate (%)')
                st.plotly_chart(fig_10y, use_container_width=True)
            with col2:
                st.markdown(get_download_links(processed_data['fed_5y'], '5y_treasury_rate'), unsafe_allow_html=True)
                fig_5y = create_line_graph(processed_data['fed_5y'], '5-Year Treasury Rate', 'Interest Rate (%)')
                st.plotly_chart(fig_5y, use_container_width=True)
                
                st.markdown(get_download_links(processed_data['fed_30y'], '30y_treasury_rate'), unsafe_allow_html=True)
                fig_30y = create_line_graph(processed_data['fed_30y'], '30-Year Treasury Rate', 'Interest Rate (%)')
                st.plotly_chart(fig_30y, use_container_width=True)

        with tabs[2]:
            st.header("Unemployment Rate")
            st.write("""
            The unemployment rate represents the number of unemployed as a percentage of the labor force.
            It is a lagging indicator, which means it measures the effect of economic events.
            """)
            st.markdown(get_download_links(processed_data['unemployment'], 'unemployment_data'), unsafe_allow_html=True)
            fig_unemployment = create_line_graph(processed_data['unemployment'], 'Unemployment Rate', 'Unemployment Rate (%)')
            st.plotly_chart(fig_unemployment, use_container_width=True)

        with tabs[3]:
            st.header("Farm Income")
            st.write("""
            Farm income represents the total income derived from agricultural activities.
            It's an important indicator of the economic health of the agricultural sector.
            """)
            st.markdown(get_download_links(processed_data['farm_income'], 'farm_income_data'), unsafe_allow_html=True)
            fig_farm_income = create_line_graph(processed_data['farm_income'], 'Farm Income', 'Billions of Dollars')
            st.plotly_chart(fig_farm_income, use_container_width=True)

        with tabs[4]:
            st.header("Gross Domestic Product (GDP)")
            st.write("""
            Gross Domestic Product (GDP) is the total monetary or market value of all the finished goods and services produced within a country's borders in a specific time period.
            It is a broad measure of overall domestic production and a key indicator of economic health.
            """)
            st.markdown(get_download_links(processed_data['gdp'], 'gdp_data'), unsafe_allow_html=True)
            fig_gdp = create_line_graph(processed_data['gdp'], 'Gross Domestic Product (GDP)', 'Billions of Dollars')
            st.plotly_chart(fig_gdp, use_container_width=True)

        with tabs[5]:
            st.header("Other Indicators")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Industrial Production Index")
                st.write("""
                The Industrial Production Index measures real output for all facilities located in the United States manufacturing, mining, and electric, and gas utilities (excluding those in U.S. territories).
                """)
                st.markdown(get_download_links(processed_data['industrial_production'], 'industrial_production_data'), unsafe_allow_html=True)
                fig_industrial = create_line_graph(processed_data['industrial_production'], 'Industrial Production Index', 'Percentage Change from Base Year')
                st.plotly_chart(fig_industrial, use_container_width=True)

                st.subheader("Housing Starts")
                st.write("""
                Housing Starts measures the number of new residential construction projects that have begun during any particular month.
                It's a key indicator of economic strength and growth.
                """)
                st.markdown(get_download_links(processed_data['housing_starts'], 'housing_starts_data'), unsafe_allow_html=True)
                fig_housing = create_line_graph(processed_data['housing_starts'], 'Housing Starts', 'Thousands of Units')
                st.plotly_chart(fig_housing, use_container_width=True)

            with col2:
                st.subheader("Retail Sales")
                st.write("""
                Retail Sales measures the total receipts at stores that sell merchandise and related services to final consumers.
                It's a key indicator of consumer spending, which drives much of the economy.
                """)
                st.markdown(get_download_links(processed_data['retail_sales'], 'retail_sales_data'), unsafe_allow_html=True)
                fig_retail = create_line_graph(processed_data['retail_sales'], 'Retail Sales', 'Millions of Dollars')
                st.plotly_chart(fig_retail, use_container_width=True)

        with tabs[6]:
            st.header("Compare Indicators")
            st.write("Select multiple indicators to compare on the same graph.")
            
            indicators = st.multiselect(
                "Select indicators to compare",
                ["CPI", "PPI", "Unemployment Rate", "2-Year Treasury Rate", "5-Year Treasury Rate", "10-Year Treasury Rate", "30-Year Treasury Rate", "Farm Income", "GDP", "Industrial Production", "Retail Sales", "Housing Starts"],
                ["CPI", "PPI", "Unemployment Rate"]  # Default selection
            )
            
            if indicators:
                comparison_data = {}
                for indicator in indicators:
                    if indicator == "CPI":
                        comparison_data[indicator] = processed_data['cpi']
                    elif indicator == "PPI":
                        comparison_data[indicator] = processed_data['ppi']
                    elif indicator == "Unemployment Rate":
                        comparison_data[indicator] = processed_data['unemployment']
                    elif indicator == "2-Year Treasury Rate":
                        comparison_data[indicator] = processed_data['fed_2y']
                    elif indicator == "5-Year Treasury Rate":
                        comparison_data[indicator] = processed_data['fed_5y']
                    elif indicator == "10-Year Treasury Rate":
                        comparison_data[indicator] = processed_data['fed_10y']
                    elif indicator == "30-Year Treasury Rate":
                        comparison_data[indicator] = processed_data['fed_30y']
                    elif indicator == "Farm Income":
                        comparison_data[indicator] = processed_data['farm_income']
                    elif indicator == "GDP":
                        comparison_data[indicator] = processed_data['gdp']
                    elif indicator == "Industrial Production":
                        comparison_data[indicator] = processed_data['industrial_production']
                    elif indicator == "Retail Sales":
                        comparison_data[indicator] = processed_data['retail_sales']
                    elif indicator == "Housing Starts":
                        comparison_data[indicator] = processed_data['housing_starts']
                
                fig_comparison = create_line_graph(comparison_data, "Indicator Comparison", "Value", is_percentage=False)
                st.plotly_chart(fig_comparison, use_container_width=True)
            else:
                st.warning("Please select at least one indicator to display the comparison graph.")

        st.markdown("---")
        st.markdown("### Data Source")
        st.markdown("All data is sourced from Federal Reserve Economic Data (FRED)")

        # Footer
        st.markdown("---")
        st.markdown(f"© {datetime.now().year} Economic Indicator Dashboard Team. All rights reserved.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

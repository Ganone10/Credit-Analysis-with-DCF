import yfinance as yf
import pandas as pd
import streamlit as st
import requests

# Replace with your EOD API key
API_KEY_1 = ' 67440c76583c64.29559846'

# Function to fetch financial data from EOD
def fetch_financial_data_eod(ticker, API_KEY):
    url = f"https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token={API_KEY}"

    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()

        try:

            Income_statement = pd.DataFrame(data['Financials']['Income_Statement']['yearly']).T
            Balance_sheet = pd.DataFrame(data['Financials']['Balance_Sheet']['yearly']).T
            Cash_Flow = pd.DataFrame(data['Financials']['Cash_Flow']['yearly']).T
            return  Income_statement, Balance_sheet, Cash_Flow

        except KeyError:
            #st.error(f"No data available for this ticker.")
            print("failed to fetch data")
            return None
    else:
        #st.error("Failed to fetch data. Check the ticker or API key.")
        print("failed to fetch data")
        return None



def fetch_financials(ticker):
    try:
        # Fetch financial data
        stock = yf.Ticker(ticker)
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow
        info = stock.info
        return financials, balance_sheet, cashflow, info
    except Exception as e:
        #st.error(f"Error fetching data: {e}")
        print("error fetching data")
        return None, None, None


def analyze_financials(ticker):
    # Initialize stock object
    stock = yf.Ticker(ticker)

    # Retrieve financial data
    financials = stock.financials
    info = stock.info

    # Extract revenue and gross profit
    try:
        revenue_current_year = financials.loc['Total Revenue'].iloc[0]
        revenue_previous_year = financials.loc['Total Revenue'].iloc[1]
        gross_profit_current_year = financials.loc['Gross Profit'].iloc[0]
        gross_profit_previous_year = financials.loc['Gross Profit'].iloc[1]

        # Compute profit margins
        profit_margin_current_year = (gross_profit_current_year / revenue_current_year) * 100
        profit_margin_previous_year = (gross_profit_previous_year / revenue_previous_year) * 100

        # Extract or compute EBITDA
        ebit_current_year = financials.loc['Operating Income'].iloc[0]
        ebit_previous_year = financials.loc['Operating Income'].iloc[1]
        #depreciation_amortization_current_year = financials.loc['Depreciation & Amortization'].iloc[0]
        #depreciation_amortization_previous_year = financials.loc['Depreciation & Amortization'].iloc[1]

        ebitda_current_year = financials.loc['EBITDA'].iloc[0]
        ebitda_previous_year = financials.loc['EBITDA'].iloc[1]

        # Print results
        return {
            "Current Year": {
                "Total Sales": revenue_current_year,
                "Gross Profit": gross_profit_current_year,
                "Profit Margin (%)": profit_margin_current_year,
                "EBITDA": ebitda_current_year
            },
            "Previous Year": {
                "Total Sales": revenue_previous_year,
                "Gross Profit": gross_profit_previous_year,
                "Profit Margin (%)": profit_margin_previous_year,
                "EBITDA": ebitda_previous_year
            }
        }
    except KeyError as e:
        return f"KeyError: Unable to find {e} in the financial statements."
    except Exception as e:
        return f"Error: {e}"


def calc_outputs(ticker):
    financial_calc = analyze_financials(ticker)
    # Extract data from financials_calc
    current_year = financials_calc['Current Year']
    previous_year = financials_calc['Previous Year']

    # Dynamic variables
    current_sales = current_year['Total Sales'] / 1e9  # Convert to billions
    previous_sales = previous_year['Total Sales'] / 1e9  # Convert to billions
    sales_growth = ((current_year['Total Sales'] - previous_year['Total Sales']) / previous_year['Total Sales']) * 100

    current_gross_profit = current_year['Gross Profit'] / 1e9  # Convert to billions
    gross_profit_growth = ((current_year['Gross Profit'] - previous_year['Gross Profit']) / previous_year[
        'Gross Profit']) * 100

    previous_margin = previous_year['Profit Margin (%)']
    current_margin = current_year['Profit Margin (%)']

    previous_ebitda = previous_year['EBITDA'] / 1e9  # Convert to billions
    current_ebitda = current_year['EBITDA'] / 1e9  # Convert to billions
    ebitda_growth = ((current_year['EBITDA'] - previous_year['EBITDA']) / previous_year['EBITDA']) * 100

    return current_sales, current_gross_profit
# Example usage
# ticker = "AAPL"  # Replace with the desired ticker symbol
# result = analyze_financials(ticker)
# print(result)
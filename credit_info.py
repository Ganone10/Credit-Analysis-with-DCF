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



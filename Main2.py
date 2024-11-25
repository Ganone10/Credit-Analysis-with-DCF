import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import credit_info as ci


# Replace with your EOD API key
API_KEY = ' 67440c76583c64.29559846'





## Set up of Streamlit Interface
st.title('Financial Dashboard')
st.header('Credit Analysis review:')
ticker_credit = st.text_input("Enter a ticker")
button_credit = st.button('Enter')

if button_credit:

    income_statement = ci.fetch_financial_data_eod(ticker_credit, 'income_statement')
    balance_sheet = ci.fetch_financial_data_eod(ticker_credit, 'balance_sheet')
    cash_flow = ci.fetch_financial_data_eod(ticker_credit, 'cash_flow')

    # Display Income Statement
    if income_statement is not None:
        st.subheader("Income Statement")
        st.dataframe(income_statement.astype(float).round(2))

    # Display Balance Sheet
    if balance_sheet is not None:
        st.subheader("Balance Sheet")
        st.dataframe(balance_sheet.astype(float).round(2))

    # Display Cash Flow Statement
    if cash_flow is not None:
        st.subheader("Cash Flow Statement")
        st.dataframe(cash_flow.astype(float).round(2))

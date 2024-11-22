import streamlit as st
import yfinance as yf
import pandas as pd

## Set up of Streamlit Interface
st.title('Financial Dashboard')
st.header('Credit Analysis review:')
ticker_credit = st.text_input("Enter a ticker")
button_credit = st.button('Enter')

if button_credit:
    # Create the Ticker object
    company = yf.Ticker(ticker_credit)
    # Retrieve the company information

    info = company.info
    # Extract the description
    description = info.get("longBusinessSummary", "")
    # Render the description
    st.write("ddd")
    st.write(description)






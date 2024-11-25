import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import credit_info as ci




## Set up of Streamlit Interface
st.title('Financial Dashboard')
st.header('Credit Analysis review:')
ticker_credit = st.text_input("Enter a ticker")
button_credit = st.button('Enter')

if button_credit:
    # Create the Ticker object
    #company = yf.Ticker(ticker_credit)
    financials, balance_sheet, cashflow, info = ci.fetch_financials(ticker_credit)
    # Retrieve the company information

    if info is not None:
        # Display Company Overview Section
        st.subheader(f"Company Overview: {info['longName']}")

        # Display key company details
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
        st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
        st.markdown(f"**Headquarters:** {info.get('city', 'N/A')}, {info.get('country', 'N/A')}")
        st.markdown(f"**Market Cap:** {info.get('marketCap', 'N/A'):,} USD")
        st.markdown(f"**Website:** [{info.get('website', 'N/A')}]({info.get('website', '#')})")
        st.markdown(f"**Description:** {info.get('longBusinessSummary', 'No description available.')}")

        # Optional: Display logo if available
        logo_url = info.get('logo_url')
        if logo_url:
            st.image(logo_url, width=100)
    if financials is not None:
        st.subheader(f"Financial Summary for {ticker_credit}")
        # Display Financial Statements
        st.write("### Income Statement:")
        st.dataframe(financials)

        st.write("### Balance Sheet:")
        st.dataframe(balance_sheet)

        st.write("### Cash Flow Statement:")
        st.dataframe(cashflow)

        # Extract key data
        revenue = financials.loc['Total Revenue']
        ebitda = financials.loc['EBITDA']
        total_debt = balance_sheet.loc['Total Debt']

        # Create a Plotly figure
        fig = go.Figure()

        # Add bar chart for revenue
        fig.add_trace(go.Scatter(
            x=revenue.index,
            y=revenue.values,
            name='Revenue',
            mode='lines+markers',
            line=dict(color='red', width=2, dash='dot')
        ))

        # Add line chart for EBITDA
        fig.add_trace(go.Scatter(
            x=ebitda.index,
            y=ebitda.values,
            name='EBITDA',
            mode='lines+markers',
            line=dict(color='green', width=2)
        ))

        # Add line chart for Total Debt
        fig.add_trace(go.Bar(
            x=total_debt.index,
            y=total_debt.values,
            name='Total Debt',
            marker_color='blue'

        ))

        # Update layout
        fig.update_layout(
            title=f"Revenue, EBITDA, and Debt for {ticker_credit}",
            xaxis_title="Date",
            yaxis_title="Amount (USD)",
            barmode='overlay',
            legend_title="Metrics",
            template="plotly_white"
        )

        # Display the chart
        st.plotly_chart(fig)
    else:
        st.error("Failed to fetch financial data.")





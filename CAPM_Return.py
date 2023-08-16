import datetime
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import capm_function 

st.set_page_config(page_title = "CAPM",
    page_icon = "chart_with_upwards_trend",
    layout = 'wide')

st.title('Capital Asset Pricing Model')

## Getting input from the user

col1,col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Choose 4 stocks", ('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])

with col2:
    year = st.number_input('Number of years',1,10)


## Downloading data for SP500

end = datetime.date.today()
start = datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)

SP500 = web.DataReader(['sp500'],'fred',start,end)

# print(SP500.tail())

##for storing the Close value of all the stock
close=[]
stocks_df = pd.DataFrame()
for stock in stocks_list:
    data = yf.download(stock,period = f'{year}y')
    # print(data.tail())
    stocks_df[f'{stock}'] = data['Close']
    
# print(stocks_df.head())
stocks_df.reset_index(inplace = True)
SP500.reset_index(inplace = True)
# print(stocks_df.dtypes)
# print(SP500.dtypes)

SP500.columns =['Date','sp500']
## Making the datetype of all the columns same
stocks_df['Date'] = stocks_df['Date'].apply(lambda x: str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
## Merging the dataframes

stocks_df = pd.merge(stocks_df, SP500, on='Date', how = 'inner')

# print(stocks_df)

col1, col2 = st.columns([1,1])
with col1:
    st.markdown('### Dataframe head')
    st.dataframe(stocks_df.head(), use_container_width=True)
    
with col2:
    st.markdown('### Dataframe tail')
    st.dataframe(stocks_df.tail(), use_container_width=True)
    
col1, col2 = st.columns([1,1])

with col1:
    st.markdown('### Price of all the Stocks')
    st.plotly_chart(capm_function.interactive_plot(stocks_df))
    
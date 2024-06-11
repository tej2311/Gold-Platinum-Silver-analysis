import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Load datasets
gold_prices = pd.read_csv('C:/Users/tejga/OneDrive/Documents/Gold.csv')
platinum_prices = pd.read_csv('C:/Users/tejga/OneDrive/Documents/Silver.csv')
silver_prices = pd.read_csv('C:/Users/tejga/OneDrive/Documents/Platinum.csv')


# Convert date columns to datetime and remove timezone information
gold_prices['Date'] = pd.to_datetime(gold_prices['Date']).dt.tz_localize(None)
platinum_prices['Date'] = pd.to_datetime(platinum_prices['Date']).dt.tz_localize(None)
silver_prices['Date'] = pd.to_datetime(silver_prices['Date']).dt.tz_localize(None)

# Streamlit app
st.set_page_config(page_title='Precious Metals Prices Dashboard', layout='wide')
st.title('Precious Metals Prices Dashboard')

# Sidebar for user inputs
st.sidebar.title('Filters')
selected_metal = st.sidebar.selectbox('Select Metal', ['Gold', 'Platinum', 'Silver', 'All'])
price_type_dict = {
    'Gold': gold_prices.columns[1:], 
    'Platinum': platinum_prices.columns[1:], 
    'Silver': silver_prices.columns[1:]
}
if selected_metal == 'All':
    price_type = st.sidebar.selectbox('Select Price Type', set(price_type_dict['Gold']) & set(price_type_dict['Platinum']) & set(price_type_dict['Silver']))
else:
    price_type = st.sidebar.selectbox('Select Price Type', price_type_dict[selected_metal])
date_range = st.sidebar.date_input('Select Date Range', [gold_prices['Date'].min(), gold_prices['Date'].max()])

# Convert date_range to timezone-naive datetime
start_date, end_date = pd.to_datetime(date_range[0]).tz_localize(None), pd.to_datetime(date_range[1]).tz_localize(None)

# Filter data based on user input
if selected_metal == 'Gold':
    data = gold_prices
elif selected_metal == 'Platinum':
    data = platinum_prices
elif selected_metal == 'Silver':
    data = silver_prices
else:
    data = pd.concat([gold_prices.assign(Metal='Gold'), 
                      platinum_prices.assign(Metal='Platinum'), 
                      silver_prices.assign(Metal='Silver')])

filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

# Line chart
st.subheader('Price Trends Over Time')
if selected_metal == 'All':
    fig = px.line(filtered_data, x='Date', y=price_type, color='Metal', title='Prices of Gold, Platinum, and Silver Over Time')
else:
    fig = px.line(filtered_data, x='Date', y=price_type, title=f'{selected_metal} Prices Over Time')
fig.update_layout(autosize=True, margin=dict(l=20, r=20, t=30, b=20))
st.plotly_chart(fig, use_container_width=True)

# Histogram
st.subheader('Price Distribution')
fig_hist = px.histogram(filtered_data, x=price_type, nbins=30, title=f'{selected_metal} Price Distribution')
fig_hist.update_layout(autosize=True, margin=dict(l=20, r=20, t=30, b=20))
st.plotly_chart(fig_hist, use_container_width=True)

# Box plot
st.subheader('Price Statistical Summary')
fig_box = px.box(filtered_data, y=price_type, title=f'{selected_metal} Price Box Plot')
fig_box.update_layout(autosize=True, margin=dict(l=20, r=20, t=30, b=20))
st.plotly_chart(fig_box, use_container_width=True)

# Moving Average
st.subheader('Moving Average')
window_size = st.sidebar.slider('Select Moving Average Window Size', 1, 30, 5)
filtered_data['Moving Average'] = filtered_data[price_type].rolling(window=window_size).mean()
fig_ma = px.line(filtered_data, x='Date', y='Moving Average', title=f'{selected_metal} Moving Average Price')
fig_ma.update_layout(autosize=True, margin=dict(l=20, r=20, t=30, b=20))
st.plotly_chart(fig_ma, use_container_width=True)

# Correlation Heatmap
if selected_metal == 'All':
    st.subheader('Correlation Heatmap')
    gold_filtered = gold_prices.set_index('Date')[price_type].rename('Gold').loc[start_date:end_date]
    platinum_filtered = platinum_prices.set_index('Date')[price_type].rename('Platinum').loc[start_date:end_date]
    silver_filtered = silver_prices.set_index('Date')[price_type].rename('Silver').loc[start_date:end_date]
    
    corr_data = pd.concat([gold_filtered, platinum_filtered, silver_filtered], axis=1)
    corr_data = corr_data.dropna()
    corr = corr_data.corr()
    fig_corr, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    plt.title('Correlation Heatmap of Precious Metals Prices')
    st.pyplot(fig_corr)

# Interactive Data Table
st.subheader('Data Table')
st.dataframe(filtered_data)

# Export filtered data
st.sidebar.title('Export Options')
if st.sidebar.button('Export Data as CSV'):
    filtered_data.to_csv('filtered_data.csv', index=False)
    st.sidebar.success('Data exported as filtered_data.csv')


st.subheader('Price Forecasting')
if selected_metal != 'All':
    forecast_years = st.sidebar.slider('Select Forecasting Years', 1, 5, 5)
    model = ARIMA(filtered_data[price_type], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_years * 15)
    
    forecast_dates = pd.date_range(start=filtered_data['Date'].max(), periods=forecast_years * 15, freq='D')
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecast': forecast})
    
    fig_forecast = px.line(forecast_df, x='Date', y='Forecast', title=f'{selected_metal} Price Forecast for Next {forecast_years} Years')
    fig_forecast.update_layout(autosize=True, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_forecast, use_container_width=True)
else:
    st.warning('Forecasting is only available for individual metals.')
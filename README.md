# Gold-Platinum-Silver-analysis

Overview:
This project involves creating an interactive dashboard for analyzing and forecasting the prices of precious metals, specifically gold, platinum, and silver. The dashboard is built using Streamlit, a Python library that allows for the creation of web apps for data science and machine learning. It provides various visualizations, statistical summaries, and the ability to forecast future prices using the ARIMA model.

Features:
Data Loading and Preprocessing:

Import historical price data for gold, platinum, and silver.
Convert date columns to datetime format and handle timezone information.
Interactive Filters:

Sidebar options to select the type of metal (Gold, Platinum, Silver, or All).
Ability to choose specific price types (e.g., price per ounce or kilogram in different currencies).
Date range selector to filter the data.
Visualizations:

Line Chart: Displays the price trends over time.
Histogram: Shows the distribution of prices.
Box Plot: Provides a statistical summary of prices.
Moving Average: Displays the moving average of selected prices.
Correlation Heatmap: Shows the correlation between different metals' prices when 'All' is selected.
Data Table:

Displays the filtered data in a tabular format for easy inspection.
Data Export:

Option to export the filtered data as a CSV file.
Price Forecasting:

Uses the ARIMA model to predict future prices for the next 1 to 10 years.
Interactive slider to select the number of forecasting years.
Technologies Used:
Python: The primary programming language.
Pandas: For data manipulation and analysis.
Plotly: For creating interactive visualizations.
Seaborn and Matplotlib: For additional data visualization.
Streamlit: For building the interactive web application.
Statsmodels: For implementing the ARIMA forecasting model.

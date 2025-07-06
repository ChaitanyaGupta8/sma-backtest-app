import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Reuse your existing function
def back_test_sma_strategy(ticker, start_date, end_date, short_window=50, long_window=200, plot=True, priceplot=True):
    data = yf.download(ticker, start=start_date, end=end_date)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)

    data = data[['Close']].copy()
    data = data.reset_index()

    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()

    data['Signal'] = 0
    data.loc[data['SMA_short'] > data['SMA_long'], 'Signal'] = 1
    data.loc[data['SMA_short'] < data['SMA_long'], 'Signal'] = -1
    data['Position'] = data['Signal'].shift(1).fillna(0)

    data['Market_returns'] = data['Close'].pct_change()
    data['Strategy_returns'] = data['Position'] * data['Market_returns']

    cumulative_strategy = (1 + data['Strategy_returns']).cumprod()
    cumulative_market = (1 + data['Market_returns']).cumprod()
    total_return = cumulative_strategy.iloc[-1] - 1
    sharpe_ratio = data['Strategy_returns'].mean() / data['Strategy_returns'].std() * np.sqrt(252)

    st.subheader("Performance Metrics")
    st.write(f"**Total Return:** {total_return:.2%}")
    st.write(f"**Sharpe Ratio:** {sharpe_ratio:.2f}")

    # Plot
    buy_signals = data[(data['Position'] == 1) & (data['Position'].shift(1) != 1)]
    sell_signals = data[(data['Position'] == -1) & (data['Position'].shift(1) != -1)]

    if plot:
        st.subheader("Cumulative Returns")
        fig1, ax1 = plt.subplots()
        ax1.plot(cumulative_strategy, label='Strategy')
        ax1.plot(cumulative_market, label='Buy & Hold')
        ax1.legend()
        ax1.set_title("Cumulative Returns")
        ax1.set_xlabel("Days")
        ax1.set_ylabel("Growth of $1")
        ax1.grid(True)
        st.pyplot(fig1)

    if priceplot:
        st.subheader("Price Chart with Signals")
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        ax2.plot(data['Date'], data['Close'], label='Close Price', color='black', alpha=0.6)
        ax2.plot(data['Date'], data['SMA_short'], label=f'Short SMA ({short_window})', color='blue', alpha=0.7)
        ax2.plot(data['Date'], data['SMA_long'], label=f'Long SMA ({long_window})', color='red', alpha=0.7)
        ax2.scatter(buy_signals['Date'], buy_signals['Close'], label='Buy Signal', marker='^', color='green', s=100)
        ax2.scatter(sell_signals['Date'], sell_signals['Close'], label='Sell Signal', marker='v', color='red', s=100)
        ax2.set_title('Moving Average Crossover Signals')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Price')
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

# Streamlit UI
st.title("SMA Crossover Strategy Backtester")

ticker = st.text_input("Ticker Symbol", value='AAPL')
start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2024-12-31"))
short_window = st.number_input("Short Window (SMA)", min_value=1, max_value=100, value=50)
long_window = st.number_input("Long Window (SMA)", min_value=10, max_value=300, value=200)

plot_returns = st.checkbox("Show Cumulative Returns", value=True)
plot_price = st.checkbox("Show Price Chart with Buy/Sell Signals", value=True)

if st.button("Run Backtest"):
    back_test_sma_strategy(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        short_window=short_window,
        long_window=long_window,
        plot=plot_returns,
        priceplot=plot_price
    )

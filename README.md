# 📈 SMA Backtest App

This is a Streamlit web app for backtesting a simple **SMA (Simple Moving Average) crossover strategy** on any stock using data from Yahoo Finance.

## 🚀 Live Demo

👉 [Click here to open the app](https://sma-backtest-app-cg.streamlit.app/)

---

## 📊 Features

- Select any **stock ticker**
- Choose your **date range**
- Customize **short and long moving averages**
- View:
  - Strategy performance vs. Buy & Hold
  - Buy/Sell signals on price chart
- **Interactive** and fully web-based (no installation needed)

---

## ⚙️ How It Works

This app uses the following logic:

1. Fetch historical stock prices using `yfinance`
2. Calculate:
   - Short-term SMA (e.g., 50 days)
   - Long-term SMA (e.g., 200 days)
3. Generate signals:
   - **Buy** when short SMA > long SMA
   - **Sell** when short SMA < long SMA
4. Plot:
   - Cumulative returns of strategy vs. market
   - Price chart with buy/sell markers

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)

---

## 📁 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

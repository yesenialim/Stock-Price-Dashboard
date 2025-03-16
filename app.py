import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to fetch stock data
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")  # Fetch last 6 months of data
    return df

@app.route("/", methods=["GET", "POST"])
def index():
    graphJSON = None
    stock_ticker = ""

    if request.method == "POST":
        stock_ticker = request.form["ticker"]
        df = fetch_stock_data(stock_ticker)

        if not df.empty:
            # Plot Stock Prices
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Stock Price"))
            
            # Simple Moving Average (SMA)
            df["SMA_50"] = df["Close"].rolling(window=50).mean()
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], mode="lines", name="50-day SMA", line=dict(dash="dot")))

            fig.update_layout(title=f"{stock_ticker} Stock Price", xaxis_title="Date", yaxis_title="Price (USD)")
            graphJSON = fig.to_html(full_html=False)

    return render_template("index.html", graphJSON=graphJSON, stock_ticker=stock_ticker)

if __name__ == "__main__":
    app.run(debug=True)

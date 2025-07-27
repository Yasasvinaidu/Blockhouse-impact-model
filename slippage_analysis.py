import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# ---------------------------------------------------------------
# Function to estimate slippage for a given order size x
# Slippage is the difference between the average execution price
# and the current mid-price, due to consuming liquidity from the book.
# ---------------------------------------------------------------
def compute_slippage(order_book, x, mid_price):
    total_cost = 0     # total execution cost
    remaining = x      # shares still to be executed

    # Loop through available volume on ask side
    for _, row in order_book.iterrows():
        price = row['ask_price_1']
        volume = row['ask_volume_1']
        qty = min(remaining, volume)     # how much can we fill at this level
        total_cost += qty * price
        remaining -= qty

        if remaining <= 0:
            break

    # If the order could not be fully filled, return NaN
    if remaining > 0:
        return np.nan

    avg_price = total_cost / x
    return avg_price - mid_price  # slippage is how far avg_price is above mid

# ---------------------------------------------------------------
# Power-law model: g(x) = α * x^δ
# Used to fit the empirical slippage values.
# ---------------------------------------------------------------
def power_model(x, alpha, delta):
    return alpha * x**delta

# ---------------------------------------------------------------
# Analyze slippage for a given stock:
# - Load LOB data
# - Compute slippage for a range of order sizes
# - Fit and plot power-law curve
# ---------------------------------------------------------------
def analyze_slippage(ticker):
    # Load CSV file (LOBSTER format: 20 columns, no header)
    df = pd.read_csv(f"data/{ticker}_lob.csv", header=None)

    # Assign column names for 5-level LOB: ask/bid prices and volumes
    df.columns = [f"{side}_{level}" 
                  for side in ["ask_price", "ask_volume", "bid_price", "bid_volume"] 
                  for level in range(1, 6)]

    # Use only the best ask level for this analysis
    order_book = df[['ask_price_1', 'ask_volume_1']].copy()

    # Mid-price is the average of best ask and best bid
    mid_price = (df['ask_price_1'].iloc[0] + df['bid_price_1'].iloc[0]) / 2

    # Define range of order sizes to simulate
    X = np.arange(10, 300, 10)  # order sizes from 10 to 290 in steps of 10

    # Compute slippage for each order size
    Y = np.array([compute_slippage(order_book, x, mid_price) for x in X])

    # Plot empirical slippage
    plt.figure(figsize=(8, 5))
    plt.plot(X, Y, marker='o', label="Empirical Slippage")
    plt.title(f"Slippage vs Order Size for {ticker}")
    plt.xlabel("Order Size (x)")
    plt.ylabel("Slippage $g_t(x)$")
    plt.grid(True)

    # Prepare data for curve fitting (ignore NaNs)
    mask = ~np.isnan(Y)
    X_fit, Y_fit = X[mask], Y[mask]

    if len(Y_fit) < 3:
        print(f"{ticker}: Not enough data points for fitting.")
        return

    # Fit power-law curve
    popt, _ = curve_fit(power_model, X_fit, Y_fit)
    alpha, delta = popt
    print(f"{ticker}: α = {alpha:.5f}, δ = {delta:.2f}")

    # Plot fitted curve
    Y_model = power_model(X_fit, *popt)
    plt.plot(X_fit, Y_model, '--', label=f"Fit: α={alpha:.4f}, δ={delta:.2f}")
    plt.legend()
    plt.tight_layout()

    # Save plot to file
    output_path = f"{ticker}_slippage_fit.png"
    plt.savefig(output_path)
    print(f"Saved plot: {output_path}")
    plt.show()

# ---------------------------------------------------------------
# Main driver: Run slippage analysis for all three stocks
# ---------------------------------------------------------------
if __name__ == "__main__":
    tickers = ["AMZN", "MSFT", "GOOG"]
    for ticker in tickers:
        file_path = f"data/{ticker}_lob.csv"
        if not os.path.exists(file_path):
            print(f"Missing data file: {file_path}")
        else:
            analyze_slippage(ticker)

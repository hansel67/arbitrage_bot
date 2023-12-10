import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yfinance as yf

# Initial account balance
balance = 1000.0

# Transaction fee (assume 0.1%)
fee = 0.001

# Download historical data for Bitcoin in USD
data = yf.download('BTC-USD', start='2020-01-01', end='2023-01-01')

# Calculate log returns
log_returns = np.log(data['Close'] / data['Close'].shift(1))

# Calculate drift and volatility
drift = log_returns.mean()
volatility = log_returns.std()

# Prices at two exchanges (initialized to last available price)
price1 = [data['Close'].iloc[-1]]
price2 = [data['Close'].iloc[-1]]

# Account balance history
balance_hist = [balance]

# Transactions history
transactions = []

def random_walk(prev_price):
    """Simulate a random walk with drift."""
    return prev_price * np.exp(drift + volatility * np.random.normal())

def arbitrage_bot():
    """Implement the arbitrage bot logic."""
    global balance
    if price1[-1] < price2[-1] * (1 - fee):
        # Buy at exchange 1 and sell at exchange 2
        amount = balance / price1[-1]
        balance -= amount * price1[-1] * (1 + fee)
        balance += amount * price2[-1] * (1 - fee)
        transactions.append((amount, price1[-1], price2[-1]))
    elif price2[-1] < price1[-1] * (1 - fee):
        # Buy at exchange 2 and sell at exchange 1
        amount = balance / price2[-1]
        balance -= amount * price2[-1] * (1 + fee)
        balance += amount * price1[-1] * (1 - fee)
        transactions.append((amount, price2[-1], price1[-1]))
    balance_hist.append(balance)

def animate(i):
    """Update the price data and account balance."""
    price1.append(random_walk(price1[-1]))
    price2.append(random_walk(price2[-1]))
    arbitrage_bot()
    ax1.clear()
    ax2.clear()
    ax1.plot(price1, label='Exchange 1')
    ax1.plot(price2, label='Exchange 2')
    ax1.legend()
    ax2.plot(balance_hist, label='Account Balance', color='r')
    ax2.legend()

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ani = animation.FuncAnimation(fig, animate, interval=100)

plt.show()

for i, (amount, buy_price, sell_price) in enumerate(transactions):
    print(f"Transaction {i + 1}: Bought {amount} at {buy_price}, Sold at {sell_price}")

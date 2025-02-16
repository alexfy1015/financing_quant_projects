# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:07:25 2025

@author: tidus
"""

import numpy as np

# Parameters
S0 = 100      # Initial stock price
r = 0.02      # Risk-free rate (3%)
q = 0.02      # Dividend yield (2%)
sigma = 0.2   # Volatility (20%)
T = 1         # Maturity in years
N = 252       # Number of time steps (daily)
M = 10000     # Number of Monte Carlo simulations
lambda_f = 0.005  # Financing spread (1%)
notional = 1e6   # Notional amount

# Time step size
dt = T / N

# Simulate stock price paths using Geometric Brownian Motion
np.random.seed(42)
Z = np.random.randn(M, N)  # Random normal variables for each path
S = np.zeros((M, N+1))
S[:, 0] = S0

for t in range(1, N+1):
    S[:, t] = S[:, t-1] * np.exp((r - q - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t-1])

# Compute the total return leg (final stock price + dividends)
ST = S[:, -1]  # Stock price at maturity
D_T = S0 * (np.exp(q * T) - 1)  # Accrued dividends

total_return_leg = notional * ((ST + D_T) / S0 - 1)

# Compute the floating leg (discounted cash flows)
floating_leg = notional * (1 - np.exp(-(r + lambda_f) * T))

# Equity swap value (expected difference between legs)
swap_value = np.mean(total_return_leg - floating_leg)

print(f"Equity Swap Value: ${swap_value:,.2f}")

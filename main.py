import riskfolio as rp
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# 1. Téléchargement des données
assets = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN', "NKE", "NVDA", "SBUX", "BA"] 
data = yf.download(assets, start='2022-11-01', end='2025-01-01', auto_adjust=True)

if isinstance(data.columns, pd.MultiIndex):
    data = data['Close']

data = data.dropna(axis=1, how='all').dropna()

# 2. Calculs Riskfolio
Y = data.pct_change().dropna()
port = rp.Portfolio(returns=Y)
port.assets_stats(method_mu='hist', method_cov='hist')

# 3. Optimisation
w = port.optimization(model='Classic', rm='MV', obj='Sharpe', rf=0, l=0, hist=True)

# 4. Simulation Monte Carlo
port_returns = (Y * w.T.values).sum(axis=1)
mu_p, sigma_p = port_returns.mean(), port_returns.std()
n_simulations, n_days, start_price = 1000, 252, 1000

random_returns = np.random.normal(mu_p, sigma_p, (n_days, n_simulations))
price_paths = np.zeros((n_days, n_simulations))
price_paths[0] = start_price

for t in range(1, n_days):
    price_paths[t] = price_paths[t-1] * (1 + random_returns[t])

print("Optimisation terminée. Les graphiques sont prêts.")

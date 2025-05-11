import numpy as np

def calculate_efficient_frontier(returns, cov_matrix, num_portfolios=10000):
    #marcador para calcular el benchmark de eficiencia.
    results = []
    for x in range(num_portfolios):
        weights = np.random.random(len(returns))
        weights = weights / np.sum(weights)
        portfolio_returns = np.sum(returns * weights) * 252
        volatilidad_portfolio = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
        results.append([portfolio_returns, volatilidad_portfolio, weights])
    return results
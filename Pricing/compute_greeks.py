import scipy.stats as stats
import numpy as np

# Black-Scholes

# Add comments

def d1(S, K, sigma, r, T):
    return (np.log(S / K) + (r + sigma*sigma / 2)*T) / sigma * np.sqrt(T)

def d2(S, K, sigma, r, T):
    return (np.log(S / K) + (r - sigma*sigma / 2)*T) / sigma * np.sqrt(T)

# TTE is taken as % of the year (Assumed to be 365 for this project)

class Call:

    def price(S, K, sigma, r, T):
        if T == 0:
            return max(0, S - K)
        else:
            return S * stats.norm.cdf(d1(S, K, sigma, r, T)) - K*np.exp(-1*r*T)*stats.norm.cdf(d2(S, K, sigma, r, T))

    # How much a price of an option changes with 1$ movement in the underlying
    def delta(S, K, sigma, r, T):
        return stats.norm.cdf(d1(S, K, sigma, r, T))

    # The velocity of delta (How much delta changes with 1$ movement in the underlying)
    def gamma(S, K, sigma, r, T):
        return stats.norm.pdf(d1(S, K, sigma, r, T)) / (S * sigma * np.sqrt(T))

    # How much a price of an option changes with 1% change in IV
    def vega(S, K, sigma, r, T):
        return (S * stats.norm.pdf(d1(S, K, sigma, r, T)) * np.sqrt(T)) / 100

    # Time value of an option (How much time value is the option losing per 1 day?)
    def theta(S, K, sigma, r, T):
        pt1 = (S * stats.norm.pdf(d1(S, K, sigma, r, T)) * sigma) / (2 * np.sqrt(T))
        pt2 = r * K * np.exp(-1*r*T) * stats.norm.cdf(d2(S, K, sigma, r, T))
        return (-1 * pt1 - 1 * pt2) / 100

    # How is the price of an option affected by the changes in risk-free interest rate
    def rho(S, K, sigma, r, T):
        return K * T * np.exp(-1* r * T) * stats.norm.cdf(d2(S, K, sigma, r, T)) / 100


class Put:

    def price(S, K, sigma, r, T):
        if T == 0:
            return max(0, S - K)
        else:
            return K * np.exp(-1 * r * T) - S * stats.norm.cdf(-1 * d1(S, K, sigma, r, T))

    # How much a price of an option changes with 1$ movement in the underlying
    def delta(S, K, sigma, r, T):
        return stats.norm.cdf(d1(S, K, sigma, r, T)) - 1

    # The velocity of delta (How much delta changes with 1$ movement in the underlying)
    def gamma(S, K, sigma, r, T):
        return stats.norm.pdf(d1(S, K, sigma, r, T)) / (S * sigma * np.sqrt(T))

    # How much a price of an option changes with 1% change in IV
    def vega(S, K, sigma, r, T):
        return (S * stats.norm.pdf(d1(S, K, sigma, r, T)) * np.sqrt(T)) / 100

    # Time value of an option (How much time value is the option losing per 1 day?)
    def theta(S, K, sigma, r, T):
        pt1 = (S * stats.norm.pdf(d1(S, K, sigma, r, T)) * sigma) / (2 * np.sqrt(T))
        pt2 = r * K * np.exp(-1*r*T) * stats.norm.cdf(-1 * d2(S, K, sigma, r, T))
        return (-1 * pt1 + pt2) / 100

    # How is the price of an option affected by the changes in risk-free interest rate
    def rho(S, K, sigma, r, T):
        return -1 * K * T * np.exp(-1 * r * T) * stats.norm.cdf(-1 * d2(S, K, sigma, r, T)) / 100


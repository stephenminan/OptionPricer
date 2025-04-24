"""
Option Pricer Class
"""
import numpy as np
import scipy as scp
from scipy.sparse.linalg import spsolve
from scipy import sparse
import scipy.stats as ss
from time import time

from OptionsContract import ContractParam


class Pricer:
    """
    Option Pricer class for representing option pricing models.
    European options:
        - Black-Scholes
        - Binomial Tree
        - Monte Carlo
    American options:
        - Binomial Tree
        - Black-Scholes PDE
    """

    def __init__(self,
                 ContractParam,
                 r: float = 0.1,
                 sigma: float = 0.2,
                 mu: float = 0.1):
        """
        :param ContractParam:
        S0 = current stock price
        K = Strike price
        T = time to maturity
        payoff = call or put
        exercise = european or american
        :param r: constant risk-free rate
        :param sigma: constant volatility
        :param mu: constant drift rate
        """

        self.S0 = ContractParam.S0
        self.K = ContractParam.K
        self.T = ContractParam.T
        self.exercise = ContractParam.exercise
        self.payoff = ContractParam.payoff
        self.dividend_yield = ContractParam.dividend_yield

        self.price = 0
        self.price_vector = 0
        self.S_vec = None

        self.r = r
        self.sigma = sigma
        self.mu = mu

    def _rvs(self, N):
        W = ss.norm.rvs((self.r - 0.5 * self.sigma**2) * self.T,
                        np.sqrt(self.T) * self.sigma, N)
        S_T = self.S0 * np.exp(W)
        return S_T.reshape((N, 1))

    def _payoffs_calculation(self, S):
        if self.payoff == "call":
            _payoffs = np.maximum(S - self.K, 0)
        elif self.payoff == "put":
            _payoffs = np.maximum(self.K - S, 0)
        return _payoffs

    def black_scholes(self):
        """
        Black-Scholes formula for European option pricing.
        Returns:
            option price: float
        """

        # Calculate D1.
        d1 = (np.log(self.S0 / self.K) + (self.r - self.dividend_yield + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))

        # Calculate D2.
        d2 = (d1 - self.sigma * np.sqrt(self.T))

        if self.payoff == 'call':
            return (self.S0 * np.exp(-self.dividend_yield * self.T) *
                    ss.norm.cdf(d1) - self.K * np.exp(-self.r * self.T) *
                    ss.norm.cdf(d2))
        else:
            return (self.K * np.exp(-self.r * self.T) *
                    ss.norm.cdf(-d2) - self.S0 *
                    np.exp(-self.dividend_yield * self.T) *
                    ss.norm.cdf(-d1))

    def binomial_tree(self, N: int = 1000):
        """
        Binomial Tree model for European and American option pricing.
        Parameters:
            N: Number of time steps
        Returns:
            option price: float
        """

        dT = float(self.T) / N  # Delta t
        u = np.exp(self.sigma * np.sqrt(dT))  # up factor
        d = 1.0 / u  # down factor

        # initialize the price vector
        self.price_vector = np.zeros(N + 1)

        # price S_T at time T
        S_T = np.array([(self.S0 * u**j * d ** (N - j)) for j in range(N + 1)])

        a = np.exp(self.r * dT)  # risk-free compound return
        p = (a - d) / (u - d)  # risk neutral up probability
        q = 1.0 - p  # risk neutral down probability

        if self.payoff == "call":
            self.price_vector[:] = np.maximum(S_T - self.K, 0.0)
        else:
            self.price_vector[:] = np.maximum(self.K - S_T, 0.0)

        for i in range(N - 1, -1, -1):
            # the price vector is overwritten at each step
            self.price_vector[:-1] = (np.exp(-self.r * dT) *
                                      (p * self.price_vector[1:] + q *
                                       self.price_vector[:-1]))
            if self.exercise == "european":
                # for european options, we do not need to check the payoff
                continue
            else:
                # for american options, we need to check the payoff
                S_T = S_T * u
                if self.payoff == "call":
                    self.price_vector = np.maximum(self.price_vector, S_T - self.K)
                else:
                    self.price_vector = np.maximum(self.price_vector, self.K - S_T)

        return self.price_vector[0]

    def monte_carlo(self,
                    simulations_num: int = 10000,
                    num_time_steps: int = 100):
        """
        Monte Carlo simulation for European option pricing.
        Parameters:
            simulations_num: Number of simulation paths
            num_time_steps: Number of time steps
        Returns:
            option price: float
        """

        # Calculate parameters
        dt = self.T / num_time_steps # Time step.
        discount_factor = np.exp(-self.r * self.T) # Discount factor.

        # Generate random paths for stock prices
        z = np.random.normal(0, 1, (simulations_num, num_time_steps)) # Standard normal random variables, uses random gen.
        stock_paths = np.zeros((simulations_num, num_time_steps + 1)) # Stock price paths.
        stock_paths[:, 0] = self.S0 # Initial stock price.

        for v in range(1, num_time_steps + 1): # Loop through time steps.
            # Calculate stock-price at each time step using geometric Brownian motion formula.
            stock_paths[:, v] = (stock_paths[:, v-1] * np.exp((self.r - self.dividend_yield - 0.5 * self.sigma**2) * dt + self.sigma * np.sqrt(dt) * z[:, v-1]))
        # Calculate payoffs
        if self.payoff == 'call':
            payoffs = np.maximum(0, stock_paths[:, -1] - self.K)
        else:
            payoffs = np.maximum(0, self.K - stock_paths[:, -1])
        # Calculate option price.
        option_value = discount_factor * np.mean(payoffs) # Discount factor average of payoffs.
        # Return option price.
        return option_value

    def black_scholes_pde(self, steps: tuple):
        """
        Black-Scholes PDE for American option pricing.

        Parameters:
            steps: tuple with number of space steps and time steps
        Returns:
            option price: float
        """

        Nspace = steps[0]
        Ntime = steps[1]

        S_max = 6 * float(self.K)
        S_min = float(self.K) / 6
        x_max = np.log(S_max)
        x_min = np.log(S_min)
        x0 = np.log(self.S0)  # current log-price

        x, dx = np.linspace(x_min, x_max, Nspace, retstep=True)
        t, dt = np.linspace(0, self.T, Ntime, retstep=True)

        self.S_vec = np.exp(x)  # vector of S
        Payoff = self._payoffs_calculation(self.S_vec)

        V = np.zeros((Nspace, Ntime))
        if self.payoff == "call":
            V[:, -1] = Payoff
            V[-1, :] = np.exp(x_max) - self.K * np.exp(-self.r * t[::-1])
            V[0, :] = 0
        else:
            V[:, -1] = Payoff
            V[-1, :] = 0
            V[0, :] = Payoff[0] * np.exp(-self.r * t[::-1])

        sig2 = self.sigma**2
        dxx = dx**2
        a = (dt / 2) * ((self.r - 0.5 * sig2) / dx - sig2 / dxx)
        b = 1 + dt * (sig2 / dxx + self.r)
        c = -(dt / 2) * ((self.r - 0.5 * sig2) / dx + sig2 / dxx)

        D = sparse.diags([a, b, c], [-1, 0, 1], shape=(Nspace - 2, Nspace - 2)).tocsc()

        offset = np.zeros(Nspace - 2)

        for i in range(Ntime - 2, -1, -1):
            offset[0] = a * V[0, i]
            offset[-1] = c * V[-1, i]
            V[1:-1, i] = np.maximum(spsolve(D, (V[1:-1, i + 1] - offset)), Payoff[1:-1])

        self.price = np.interp(x0, x, V[:, 0])

        return self.price

"""
Options Class
"""


class ContractParam:
    """
    Class for representing option contract
    parameters:
        S0 = current stock price
        K = Strike price
        T = time to maturity
        v0 = (optional) spot variance
        dividend_yield = (optional) dividend yield
        payoff = call or put
        exercise = european or american
    """

    def __init__(self,
                 S0: float,
                 K: float,
                 T: float,
                 v0: float = 0.04,
                 dividend_yield: float = 0.0,
                 payoff: str = "call",
                 exercise: str = "european"):
        self.S0 = S0
        self.K = K
        self.T = T
        self.v0 = v0
        self.dividend_yield = dividend_yield
        self.payoff = payoff
        self.exercise = exercise

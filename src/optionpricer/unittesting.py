import unittest
import OptionsContract
import Pricer


class TestOptionPricing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # parameters for the tests
        cls.S0, cls.K, cls.T = 100, 105, 1.0
        cls.r, cls.sigma, cls.dividend_yield = 0.05, 0.2, 0.0
        cls.call_option_param = OptionsContract.ContractParam(
            S0=cls.S0,
            K=cls.K,
            T=cls.T,
            dividend_yield=cls.dividend_yield,
            payoff="call",
            exercise="european"
        )
        cls.put_option_param = OptionsContract.ContractParam(
            S0=cls.S0,
            K=cls.K,
            T=cls.T,
            dividend_yield=cls.dividend_yield,
            payoff="put",
            exercise="european"
        )
        cls.call_pricer = Pricer.Pricer(cls.call_option_param, cls.r, cls.sigma)
        cls.put_pricer = Pricer.Pricer(cls.put_option_param, cls.r, cls.sigma)
        # Expected
        cls.expected_call = 8.0214 
        cls.expected_put = 7.9000
        cls.tolerance = 0.50 

    def test_black_scholes(self):
        """
        Test Black-Scholes model with expected
        """
        call = self.call_pricer.black_scholes()
        put = self.put_pricer.black_scholes()
        self.assertAlmostEqual(call, self.expected_call, places=3)
        self.assertAlmostEqual(put, self.expected_put, places=3)

    def test_binomial_tree(self):
        """
        Test binomial tree approximation with expected
        """
        call = self.call_pricer.binomial_tree(N=100)
        put = self.put_pricer.binomial_tree(N=100)
        self.assertAlmostEqual(call, self.expected_call, delta=self.tolerance)
        self.assertAlmostEqual(put, self.expected_put, delta=self.tolerance)

    def test_monte_carlo(self):
        """
        Test Monte Carlo simulation with expected
        """
        call = self.call_pricer.monte_carlo()
        put = self.put_pricer.monte_carlo()
        self.assertAlmostEqual(call, self.expected_call, delta=self.tolerance)
        self.assertAlmostEqual(put, self.expected_put, delta=self.tolerance)


if __name__ == '__main__':
    unittest.main()

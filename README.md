# OptionPricer

OptionPricer is a Python library for pricing financial options using the Black-Scholes formula and the Binomial Tree model. It supports both American and European options, providing a simple and efficient way to calculate option prices.

## Features

- **Black-Scholes Formula**: Analytical pricing for European options.
- **Binomial Tree Model**: Numerical pricing for both American and European options.
- Support for call and put options.
- Flexible input parameters for customization.

## Installation

Use the package manager [**pip**](https://pip.pypa.io/en/stable/) to install OptionPricer.

```bash
pip install optionpricer
```

## Usage
### Black-Scholes Formula

```python
from optionpricer.black_scholes import black_scholes

# Example: Price a European call option
price = black_scholes(
    option_type="call",
    spot_price=100,
    strike_price=110,
    time_to_maturity=1,
    risk_free_rate=0.05,
    volatility=0.2
)
print(f"Option Price: {price}")
```
### Binomial Tree Model

```python
from optionpricer.binomial_tree import binomial_tree

# Example: Price an American call option
price = binomial_tree(
    option_type="call",
    spot_price=100,
    strike_price=110,
    time_to_maturity=1,
    risk_free_rate=0.05,
    volatility=0.2,
    steps=100,
    american=True
)
print(f"Option Price: {price}")
```
```python
from optionpricer.monte_carlo import monte_carlo

# Example: Price a European call option
price = monte_carlo(
    option_type="call",
    spot_price=100,
    strike_price=110,
    time_to_maturity=1,
    risk_free_rate=0.05,
    volatility=0.2,
    steps=100,
    american=False
)
print(f"Option Price: {price}")
```
### How to run this package (SUPER SIMPLE)
-Install package.
-Import and initialize class.
- Download modules.
- Unittest for model functionality.
- Choose jupyter script for the style of option.
- Declare call or put and what model to use.
- Module will automatically create MAE and visualize predicted option prices for comparison.
## Contributing
[<img src="https://github.com/stephenminan.png" width="60px;"/><br /><sub><a href="https://github.com/stephenminan">Stephen An</a></sub>](https://github.com/stephenminan) 

[<img src="https://github.com/AntonioTagliatti.png" width="60px;"/><br /><sub><a href="https://github.com/AntonioTagliatti">Antonio Tagliatti</a></sub>](https://github.com/AntonioTagliatti)


## License
[MIT](https://choosealicense.com/licenses/mit/)


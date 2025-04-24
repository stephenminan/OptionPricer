# OptionPricer

OptionPricer is a Python library for pricing financial options using the Black-Scholes formula and the Binomial Tree model. It supports both American and European options, providing a simple and efficient way to calculate option prices.

## Features

- **Black-Scholes Formula**: Analytical pricing for European options.
- **Binomial Tree Model**: Numerical pricing for both American and European options.
- **Monte Carlo Model**: Numerical pricing for both American and European options.
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
### Monte Carlo Model
```python
from optionpricer.monte_carlo import monte_carlo
price = monte_carlo(
    option_type="call",
    spot_price=100,
    strike_price=110,
    time_to_maturity=1,
    risk_free_rate=0.05,
    volatility=0.2,
    steps=100,
    american=True
```
### Directions for Package
    - This package is super simple one main class with inheriting classes that have methods of models to price options
    - There are two jupyter notebook files: one for EDA on American historic data, and one for EDA on European future data.
    - The two jupyter notebooks easily lead through how to use models, and also incorporate visualization for output.
    - If you want to add models just write where other methods are and test case using test unit.
## Contributing
[<img src="https://github.com/stephenminan.png" width="60px;"/><br /><sub><a href="https://github.com/stephenminan">Stephen An</a></sub>](https://github.com/stephenminan) 

[<img src="https://github.com/AntonioTagliatti.png" width="60px;"/><br /><sub><a href="https://github.com/AntonioTagliatti">Antonio Tagliatti</a></sub>](https://github.com/AntonioTagliatti)


## License
[MIT](https://choosealicense.com/licenses/mit/)


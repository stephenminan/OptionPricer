import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import OptionsContract
import Pricer
from helper import load_data_files, calculate_days_to_expiration
import time


def main():
    """ 
    The following code is specific to simulations by CBOE.
    What can you change in this to run what you want?
    - File you want to explore
    - Current date (Hard coded because CBOE simulates by day)
    - Risk Free rate (Can be decided by user)
    - Dividend Yield (Can be decided by user)
    - Option type (Call or Put)
    - Model to use (Black-Scholes, Binomial Tree, Monte Carlo)
    """
    # Load data files
    data_frames = load_data_files('../data/raw/european')
    current_df = data_frames['spx_quotedata']

    # Params
    S0 = 5158.2002  # S&P 500 last price
    r = 0.05  # Risk-free rate
    current_date = '2025-04-21'  # Current date
    dividend_yield = 0.0  # SPX contains no dividends
    list = []  # List for storing calculated prices
    option_type = 'call'
    i = 3  # 1 = Black-Scholes, 2 = Binomial Tree, 3 = Monte Carlo
    print(i)
    print(option_type)
    # Start timer.
    start = time.perf_counter()

    # Run Models
    for index, row in current_df.iterrows():
        K = row['Strike']
        T = calculate_days_to_expiration(current_date, row['Expiration Date'])/365
        if option_type == 'call':
            # Params for Call
            sigma = row['IV']

            option_param = OptionsContract.ContractParam(S0=S0,
                                                         K=K,
                                                         T=T,
                                                         dividend_yield=dividend_yield,
                                                         payoff=option_type,
                                                         exercise='european')
        else:
            # Params for Put
            sigma = row['IV.1']

            option_param = OptionsContract.ContractParam(S0=S0,
                                                             K=K,
                                                             T=T,
                                                             dividend_yield=dividend_yield,
                                                             payoff=option_type,
                                                             exercise='european')
        pricer = Pricer.Pricer(option_param, r=r, sigma=sigma, mu=0.1)
        # Models
        if i == 1:
            price = pricer.black_scholes()
        elif i == 2:
            price = pricer.binomial_tree(N=100)
        elif i == 3:
            price = pricer.monte_carlo(100000, 100)

        list.append(round(price, 2))

    # End timer
    end = time.perf_counter()
    # Print result
    print(f"Execution time: {end - start:.6f} seconds")


    # Add the calculated prices to DataFrame, create new columns.
    current_df['My Price'] = list
    if option_type == 'call':
        current_df['My Call Price'] = current_df['My Price']
        current_df['Actual Call Price'] = (current_df['Bid'] + current_df['Ask']) / 2
        current_df['Call Absolute Error'] = abs((current_df['My Price'] - current_df['Actual Call Price']))
        mean_abs_error = current_df['Call Absolute Error'].mean()
        print(mean_abs_error)
    else:
        current_df['My Put Price'] = current_df['My Price']
        current_df['Actual Put Price'] = (current_df['Bid.1'] + current_df['Ask.1']) / 2
        current_df['Put Absolute Error'] = abs((current_df['My Price'] - current_df['Actual Put Price']))
        mean_abs_error = current_df['Put Absolute Error'].mean()
        print(mean_abs_error)
    
    # New Expiration Date column with just month and day for plotting
    current_df['Expiration MD'] = pd.to_datetime(current_df['Expiration Date']).dt.strftime('%m-%d')

    # Graphing section dependned on 'call' or 'put'
    if option_type == 'call':
        sns.lineplot(data=current_df, x='Expiration MD', y='My Call Price', label='My Simulated')
        sns.lineplot(data=current_df, x='Expiration MD', y='Actual Call Price', label='CBOE Simulated')
        plt.xlabel('Expiration Date (Month-Day)')
        plt.ylabel('Option Price (USD)')
        plt.title('Option Price by Expiration Date (Call)')
        plt.xticks(rotation=45)
        plt.ylim(100, 250)
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        sns.lineplot(data=current_df, x='Expiration MD', y='My Put Price', label='My Simulated')
        sns.lineplot(data=current_df, x='Expiration MD', y='Actual Put Price', label='CBOE Simulated')
        plt.xlabel('Expiration Date (Month-Day)')
        plt.ylabel('Option Price (USD)')
        plt.ylim(0,250)
        plt.title('Option Price by Expiration Date (Put)')
        plt.xticks(rotation=45)
        plt.ylim(100,240)
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()

import os
import pandas as pd
from datetime import datetime


def load_data_files(folder_path='../data/raw/european'):
    """
    Loads all CSV files from folder.
    ADAPTED FOR CBOE SIMULATION DATA.
    Parameters:
        folder_path (str): Path to folder w/ files
    Returns:
        data_frames(dict): Keys=filenames, values= dataframes
    """
    # Create dictionary.
    data_frames = {}
    # Loop through all files in the folder.
    for filename in os.listdir(folder_path):
        # Use os to join paths.
        data_path = os.path.join(folder_path, filename)
        # Check if file is csv.
        if os.path.isdir(data_path) or not filename.endswith('.csv'):
            continue
        # Check if file name matches pattern.
        file_key = os.path.splitext(filename)[0]
        # Try to load the file.
        try:
            # Load the data and skip first 3 rows.
            df = pd.read_csv(data_path, skiprows=3)
            data_frames[file_key] = df
        # If not print error.
        except Exception as e:
            print("Error")
    return data_frames


def calculate_days_to_expiration(current_date, expiration_date):
    """
    Calculate days between current date and expiration date.
    DATE HAS TO BE FUTURE THIS IS FUTURE SIM.
    Parameters:
        current_date (str): Current date.
        expiration_date (str): Expiration date string.
    Returns:
        result(int): Number of days to expiration.
    """
    # Convert current date using datetime
    current_date = pd.to_datetime(current_date)
    try:
        # Try close format
        exp_date = datetime.strptime(expiration_date, '%a%b%d%Y')
    except ValueError:
        try:
            # If error try other format.
            exp_date = datetime.strptime(expiration_date, '%a %b %d %Y')
        # If error try other format.
        except ValueError as e:
            print("Error")
    # Calculate difference (Days)
    days_exp = (exp_date - current_date).days
    # Return the number of days if it's a future date otherwise raise error.
    if days_exp >= 0:
        result = days_exp
    else:
        raise ValueError("Date must be in future.")
    return result

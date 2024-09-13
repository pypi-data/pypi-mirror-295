import pandas as pd
import numpy as np
from lib.data_provider import DataProvider

class DataPreparation:
    """
    A class for preparing daily stock data for analysis and modeling.

    This class includes methods for processing daily stock data and creating
    features for machine learning models. It uses the DataProvider class to fetch data.

    The prepare_data method uses the specified features (Open, High, Low, Close, Volume)
    and sets the target as the next day's High price.
    """

    @staticmethod
    def prepare_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        data = DataProvider.fetch_data_for_date_range(symbol, start_date, end_date)
        
        # Ensure we have all required columns
        features = ['Open', 'High', 'Low', 'Close', 'Volume']

        # Create the binary classification target
        data['NextDayHigher'] = (data['High'].shift(-1) > data['Close']).astype(int)
        
        # Drop rows with NaN values
        data.dropna(inplace=True)
        
        # Update the target variable name
        target = ['NextDayHigher']
        
        # Get the common index
        common_index = data[features + target].dropna().index
        
        # Filter data to keep only rows with the common index
        data = data.loc[common_index]
        
        return data

if __name__ == "__main__":
    symbol = "NVDA"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    data = DataPreparation.prepare_data(symbol, start_date, end_date)
    print(data.head(20))
    print(data.columns)
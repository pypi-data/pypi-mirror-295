import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import pickle
from os import path

class DataProvider:
    """
    A class for fetching and caching daily stock data using the yfinance library.
    
    This class includes methods for fetching and processing daily stock data.
    It uses pickle-based caching to store API responses locally, improving
    performance for repeated queries.
    
    Attributes:
        CACHE_DIR (str): The directory where pickled data will be stored.
    """

    CACHE_DIR = 'data_cache'

    @staticmethod
    def get_pickle_path(symbol: str, start_date: str, end_date: str) -> str:
        if not path.exists(DataProvider.CACHE_DIR):
            os.makedirs(DataProvider.CACHE_DIR)
        
        filename = f"{symbol}_{start_date}_{end_date}.pickle"
        return path.join(DataProvider.CACHE_DIR, filename)

    @staticmethod
    def fetch_daily_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        pickle_path = DataProvider.get_pickle_path(symbol, start_date, end_date)
        
        if path.exists(pickle_path):
            with open(pickle_path, 'rb') as f:
                return pickle.load(f)

        df = yf.download(symbol, start=start_date, end=end_date)
        
        # Ensure the DataFrame has the expected columns
        expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = df[expected_columns]

        with open(pickle_path, 'wb') as f:
            pickle.dump(df, f)

        return df

    @staticmethod
    def fetch_data_for_date_range(symbol: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        return DataProvider.fetch_daily_data(symbol, start_date, end_date)
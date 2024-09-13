import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from lib.base import ScalerStrategy

class StandardScalerStrategy(ScalerStrategy):
    def __init__(self):
        self.scalers = {}

    def fit_transform(self, X):
        self.scalers = {column: StandardScaler() for column in X.columns}
        return pd.DataFrame({column: self.scalers[column].fit_transform(X[[column]]).flatten() 
                             for column in X.columns}, index=X.index)

    def transform(self, X):
        return pd.DataFrame({column: self.scalers[column].transform(X[[column]]).flatten() 
                             for column in X.columns}, index=X.index)

class MinMaxScalerStrategy(ScalerStrategy):
    def __init__(self):
        self.scalers = {}

    def fit_transform(self, X):
        self.scalers = {column: MinMaxScaler() for column in X.columns}
        return pd.DataFrame({column: self.scalers[column].fit_transform(X[[column]]).flatten() 
                             for column in X.columns}, index=X.index)

    def transform(self, X):
        return pd.DataFrame({column: self.scalers[column].transform(X[[column]]).flatten() 
                             for column in X.columns}, index=X.index)

class RobustScalerStrategy(ScalerStrategy):
    def __init__(self):
        self.scalers = {}

    def fit_transform(self, X):
        self.scalers = {column: RobustScaler() for column in X.columns}
        return pd.DataFrame({column: self.scalers[column].fit_transform(X[[column]]).flatten() 
                             for column in X.columns}, index=X.index)

    def transform(self, X):
        return pd.DataFrame({column: self.scalers[column].transform(X[[column]]).flatten() 
                             for column in X.columns}, index=X.index)

class NoScalingStrategy(ScalerStrategy):
    def fit_transform(self, X):
        return X

    def transform(self, X):
        return X
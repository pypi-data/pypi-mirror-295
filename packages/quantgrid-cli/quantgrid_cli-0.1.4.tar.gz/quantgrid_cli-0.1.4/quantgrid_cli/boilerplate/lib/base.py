import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict

class TimeSeriesModel(ABC):
    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        pass

class ScanStrategy(ABC):
    @abstractmethod
    def generate_windows(self, data: pd.DataFrame, **kwargs) -> List[Dict]:
        pass

class Metric(ABC):
    @abstractmethod
    def calculate(self, actual: pd.Series, predicted: np.ndarray) -> float:
        pass

class ScalerStrategy(ABC):
    @abstractmethod
    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        pass
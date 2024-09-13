from lib.base import ScanStrategy
import pandas as pd

def ensure_datetime_consistency(data):
    """
    Ensure that the DataFrame's index is timezone-naive.
    If it's timezone-aware, convert to naive by removing the timezone info.
    """
    if isinstance(data.index, pd.DatetimeIndex):
        if data.index.tzinfo is not None:
            return data.tz_localize(None)
    return data

class SlidingWindowStrategy(ScanStrategy):
    def generate_windows(self, data, window_size, step_size, horizon):
        windows = []
        data = ensure_datetime_consistency(data)
        data_length = len(data)
        
        # Iterate using step_size
        for start in range(0, data_length - window_size - horizon + 1, step_size):
            end = start + window_size
            if end + horizon <= data_length:
                windows.append({
                    'train_start': start,
                    'train_end': end,
                    'test_start': end,
                    'test_end': end + horizon
                })
        return windows
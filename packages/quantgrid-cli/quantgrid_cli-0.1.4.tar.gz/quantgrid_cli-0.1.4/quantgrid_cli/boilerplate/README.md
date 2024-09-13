# Quantgrid - MLFlow Time Series Experiment Tracking

This project is a boilerplate for creating a time series experiment tracking system using MLFlow. 
It uses yfinance to get stock data and uses a random forest model to predict the next day's outcome.

## Getting Started

### Prerequisites

- Python 3.8+
- MLFlow
- Pandas
- NumPy
- Scikit-learn

## Usage

To run the project, simply run `python main.py`

See `lib/data_preparation.py` for more information on the data preparation process.
See `lib/data_provider.py` for more information on the data provider.
See `lib/experiment_runner.py` to customize the experiment runner.
See `lib/scanner.py` for more information on the timeseries scanner.
See `lib/models.py` for  customizing the models.
See `lib/scalers.py` for more information on the scalers.
See `lib/strategies.py` for more information on the window generation strategies.
See `lib/metrics.py` for more information on the metrics.



## More Information

See quantgrid.net for more information on the project.
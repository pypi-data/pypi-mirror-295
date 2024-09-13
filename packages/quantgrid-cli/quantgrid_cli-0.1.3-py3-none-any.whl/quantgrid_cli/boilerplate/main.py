import argparse
import logging
from dotenv import load_dotenv
from lib.mlflow_utils import setup_mlflow
from lib.experiment_runner import run_experiment
from lib.scanner import TimeSeriesScanner
from lib.models import RandomForestModel
from lib.scalers import StandardScalerStrategy, MinMaxScalerStrategy, RobustScalerStrategy, NoScalingStrategy
from lib.data_preparation import DataPreparation
from lib.strategies import SlidingWindowStrategy
from lib.metrics import Accuracy
from config import get_config

logging.basicConfig(level=logging.INFO)
load_dotenv()

def process_symbol(symbol):
    logging.info(f"Processing symbol: {symbol}")
        
    config = get_config(symbol)

    try:
        
        data = DataPreparation.prepare_data(config['symbol'], config['start_date'], config['end_date'])
        data.index = data.index.tz_localize(None)

        scanners = {
            f"{scaler.__name__}": TimeSeriesScanner(data[config['features'] + [config['target']]], 
                                                    target_cols=config['target'], 
                                                    scaler_strategy=scaler())
            for scaler in [NoScalingStrategy, StandardScalerStrategy, MinMaxScalerStrategy, RobustScalerStrategy]
        }

        for scanner_name, scanner in scanners.items():
            logging.info(f"\n--- Results for {symbol} with {scanner_name} ---")
            
            run_experiment(scanner, RandomForestModel(**config['rf_params']), config['scan_params'], 
                           scanner_name, "Random Forest", config['rf_params'], config,
                           scan_strategy=SlidingWindowStrategy(), metrics=[Accuracy()])
            
            # run_experiment(scanner, CNNModel(
            #     input_shape=config['cnn_params']['input_shape'],
            #     layers=config['cnn_params']['layers'],
            #     compile_params=config['cnn_params']['compile_params'],
            #     fit_params=config['cnn_params']['fit_params']
            # ), config['scan_params'], 
            #                scanner_name, "CNN", config['cnn_params'], config,
            #                scan_strategy=SlidingWindowStrategy(), metrics=[Accuracy()])

        logging.info(f"Finished processing symbol: {symbol}")
    except Exception as e:
        logging.error(f"Error processing symbol {symbol}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Process symbols from Redis queue or command line")
    parser.add_argument("--symbol", help="Symbol to process (bypasses Redis queue)")
    args = parser.parse_args()

    try:
        setup_mlflow()
    except Exception as e:
        logging.error(f"Error setting up MLflow: {e}")
        logging.warning("Continuing without MLflow logging...")
    if not args.symbol:
        args.symbol = "NVDA"
    if args.symbol:
        # Process the symbol provided via command line
        process_symbol(args.symbol)
    else:
        # return error
        logging.error("No symbol provided")
        exit(1)

if __name__ == "__main__":
    main()
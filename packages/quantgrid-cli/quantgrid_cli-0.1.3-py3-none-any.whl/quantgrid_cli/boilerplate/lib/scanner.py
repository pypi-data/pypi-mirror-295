import pandas as pd
import numpy as np
from typing import List, Dict, Any, Union, Tuple
from concurrent.futures import ProcessPoolExecutor
from lib.base import TimeSeriesModel, ScanStrategy, Metric, ScalerStrategy
from lib.scalers import StandardScalerStrategy
from sklearn.metrics import classification_report

class TimeSeriesScanner:
    def __init__(self, data: pd.DataFrame, target_cols: Union[str, List[str]], scaler_strategy: ScalerStrategy = StandardScalerStrategy()):
        self.data = data
        self.target_cols = [target_cols] if isinstance(target_cols, str) else target_cols
        self.feature_cols = [col for col in data.columns if col not in self.target_cols]
        self._validate_data()
        self.scaler = scaler_strategy

    def _validate_data(self):
        assert all(col in self.data.columns for col in self.target_cols), "Not all target columns found in data"

    def scan(self, 
             model: TimeSeriesModel,
             scan_strategy: ScanStrategy,
             metrics: List[Metric],
             n_jobs: int = 8,
             **scan_params) -> Dict[str, Any]:
        
        windows = scan_strategy.generate_windows(self.data, **scan_params)
        total_windows = len(windows)
        
        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            results = list(executor.map(self._evaluate_window, 
                                        windows, 
                                        [model]*len(windows), 
                                        [metrics]*len(windows)))
        
        valid_windows = sum(1 for result in results if result is not None)
        overall_results, classification_reports = self._aggregate_results(results)
        
        scan_summary = {
            "total_windows": total_windows,
            "valid_windows": valid_windows
        }
        
        return overall_results, classification_reports, scan_summary

    def _evaluate_window(self, window: Dict, model: TimeSeriesModel, metrics: List[Metric]) -> Dict:
        train_data = self.data.iloc[window['train_start']:window['train_end']]
        test_data = self.data.iloc[window['test_start']:window['test_end']]
        
        X_train, y_train = train_data[self.feature_cols], train_data[self.target_cols]
        X_test, y_test = test_data[self.feature_cols], test_data[self.target_cols]
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        model.fit(X_train_scaled, y_train)
        predictions = model.predict(X_test_scaled)
        
        # Calculate classification report
        cr = classification_report(y_test, predictions, output_dict=True, zero_division=0)
        
        # Extract relevant metrics
        metrics_dict = {}
        for label in cr.keys():
            if label not in ['accuracy', 'macro avg', 'weighted avg']:
                metrics_dict[f'{label}_precision'] = cr[label]['precision']
                metrics_dict[f'{label}_recall'] = cr[label]['recall']
                metrics_dict[f'{label}_f1-score'] = cr[label]['f1-score']
        
        metrics_dict['accuracy'] = cr['accuracy']
        metrics_dict['macro_avg_precision'] = cr['macro avg']['precision']
        metrics_dict['macro_avg_recall'] = cr['macro avg']['recall']
        metrics_dict['macro_avg_f1-score'] = cr['macro avg']['f1-score']
        metrics_dict['weighted_avg_precision'] = cr['weighted avg']['precision']
        metrics_dict['weighted_avg_recall'] = cr['weighted avg']['recall']
        metrics_dict['weighted_avg_f1-score'] = cr['weighted avg']['f1-score']
        
        # Check for classes with zero predicted samples
        zero_precision_classes = [label for label, metrics in cr.items() if isinstance(metrics, dict) and metrics['precision'] == 0]
        if zero_precision_classes:
            print(f"Warning: The following classes had no predicted samples in this window: {zero_precision_classes}")
            print("This may indicate class imbalance or issues with the model's predictions.")
        
        # Add a check for valid window
        if len(X_train) == 0 or len(X_test) == 0:
            return None  # Invalid window

        return {
            'window': window,
            'metrics': {**metrics_dict, **{metric.__class__.__name__: metric.calculate(y_test.T, predictions) for metric in metrics}},
            'classification_report': cr
        }

    def _aggregate_results(self, results: List[Dict]) -> Tuple[Dict[str, Any], List[Dict]]:
        aggregated_metrics = {}
        classification_reports = []
        for result in results:
            if result is None:  # Skip invalid windows
                continue
            for metric_name, value in result['metrics'].items():
                if metric_name not in aggregated_metrics:
                    aggregated_metrics[metric_name] = []
                aggregated_metrics[metric_name].append(value)
            classification_reports.append(result['classification_report'])
        
        overall_results = {metric: np.mean(values) for metric, values in aggregated_metrics.items()}
        return overall_results, classification_reports
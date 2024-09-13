import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import pandas as pd
import numpy as np
from lib.strategies import SlidingWindowStrategy
from lib.metrics import Accuracy
import re
import logging

def run_experiment(scanner, model, scan_params, scanner_name, model_name, model_params, config,
                   scan_strategy=SlidingWindowStrategy(), metrics=[Accuracy()]):
    with mlflow.start_run(run_name=f"{scanner_name} - {model_name}"):
        # Log configuration details
        mlflow.log_params({
            "symbol": config['symbol'],
            "start_date": config['start_date'],
            "end_date": config['end_date'],
            "features": ", ".join(config['features']),
            "target": config['target'],
            "window_size": config['scan_params']['window_size'],
            "step_size": config['scan_params']['step_size'],
            "horizon": config['scan_params']['horizon']
        })

        X = scanner.data.drop(columns=scanner.target_cols)
        y = scanner.data[scanner.target_cols]


        if X.shape[0] != y.shape[0]:
            logging.error(f"Mismatch in number of samples: X has {X.shape[0]}, y has {y.shape[0]}")
            return None, None, None

        try:
            model.fit(X, y)
            mlflow.log_params(model_params)
            signature = infer_signature(X, model.predict(X))
            mlflow.sklearn.log_model(model.model, "model", signature=signature)

            results, classification_reports, scan_summary = scanner.scan(
                model=model,
                scan_strategy=scan_strategy,
                metrics=metrics,
                **scan_params
            )

            # Log scan summary metrics
            mlflow.log_param("total_windows", scan_summary["total_windows"])
            mlflow.log_param("valid_windows", scan_summary["valid_windows"])

            for metric_name, metric_value in results.items():
                mlflow.log_metric(metric_name, metric_value)

            # Calculate classification report summary
            cr_summary = calculate_classification_report_summary(classification_reports)

            # Log classification report summary metrics
            for stat in cr_summary.index:
                for metric in cr_summary.columns:
                    stat_name = clean_name(stat)
                    metric_name = clean_name(metric)
                    mlflow.log_metric(f"cr_summary_{stat_name}_{metric_name}", cr_summary.loc[stat, metric])

            # Log the entire classification report summary as a JSON artifact
            mlflow.log_dict(cr_summary.to_dict(), "classification_report_summary.json")

            print(f"{model_name} Results:", results)
            print(f"{model_name} Classification Report Summary:")
            print(cr_summary)
            print(f"{model_name} Scan Summary:")
            print(scan_summary)

            return results, cr_summary, scan_summary
        except Exception as e:
            logging.error(f"Error during model fitting: {str(e)}")
            return None, None, None

def calculate_classification_report_summary(classification_reports):
    # Flatten the nested structure and handle nan values
    flattened_reports = []
    for report in classification_reports:
        flattened_report = {}
        for key, value in report.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    flattened_report[f"{key}_{sub_key}"] = sub_value if not pd.isna(sub_value) else None
            else:
                flattened_report[key] = value if not pd.isna(value) else None
        flattened_reports.append(flattened_report)

    # Convert list of flattened dictionaries to DataFrame
    cr_df = pd.DataFrame(flattened_reports)

    # Replace None with NaN for proper statistical calculations
    cr_df = cr_df.replace({None: np.nan})

    # Calculate summary statistics
    summary = cr_df.describe()

    # Add median to the summary
    median = cr_df.median()
    summary.loc['50%'] = median

    # Add mode to the summary
    mode = cr_df.mode().iloc[0]
    summary.loc['mode'] = mode

    # Add variance to the summary
    variance = cr_df.var()
    summary.loc['variance'] = variance

    # Reorder the summary
    order = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'mode', 'variance']
    summary = summary.reindex(order)

    return summary

def clean_name(name):
    # Replace '%' with 'percentile'
    name = name.replace('%', 'percentile')
    # Remove any character that's not alphanumeric, underscore, dash, period, space, or slash
    name = re.sub(r'[^a-zA-Z0-9_\-. /]', '', name)
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    return name
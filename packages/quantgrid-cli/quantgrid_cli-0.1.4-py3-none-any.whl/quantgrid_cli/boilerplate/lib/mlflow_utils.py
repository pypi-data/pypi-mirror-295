import os
import mlflow

def setup_mlflow():
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    username = os.environ.get("MLFLOW_TRACKING_USERNAME")
    password = os.environ.get("MLFLOW_TRACKING_PASSWORD")

    if not username or not password:
        raise ValueError("MLflow credentials not found in environment variables")

    os.environ['MLFLOW_TRACKING_USERNAME'] = username
    os.environ['MLFLOW_TRACKING_PASSWORD'] = password
    mlflow.set_tracking_uri(tracking_uri)

    try:
        mlflow.search_experiments()
        print("Successfully authenticated with MLflow server")
    except mlflow.exceptions.MlflowException as e:
        print(f"Failed to authenticate with MLflow server: {e}")
        raise
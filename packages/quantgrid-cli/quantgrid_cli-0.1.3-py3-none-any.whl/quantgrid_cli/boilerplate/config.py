import pandas as pd

def get_config(symbol):
    return {
        'symbol': symbol,
        'start_date': (pd.Timestamp.now() - pd.DateOffset(years=1)).strftime('%Y-%m-%d'),
        'end_date': (pd.Timestamp.now() - pd.DateOffset(days=1)).strftime('%Y-%m-%d'),
        'features': [
            'Open',
            'High',
            'Low',
            'Close',
            'Volume'
        ],
        'target': 'NextDayHigher',
        'scan_params': {
            'window_size': 150,  # 150 trading days
            'step_size': 150,     # Move forward 150 days at a time
            'horizon': 30        # Predict the next 30 day's outcome
        },
        'rf_params': {
            'n_estimators': 100,
        },
        'cnn_params': {
            'layers': [
                {'type': 'Conv1D', 'filters': 64, 'kernel_size': 3, 'activation': 'relu'},
                {'type': 'MaxPooling1D', 'pool_size': 2},
                {'type': 'Flatten'},
                {'type': 'Dense', 'units': 64, 'activation': 'relu'},
                {'type': 'Dense', 'units': 1, 'activation': 'sigmoid'}
            ],
            'compile_params': {
                'optimizer': 'adam',
                'loss': 'binary_crossentropy',
                'metrics': ['accuracy']
            },
            'fit_params': {
                'epochs': 28,
                'batch_size': 32,
                'validation_split': 0.2
            }
        }
    }
from sklearn.ensemble import RandomForestClassifier
from lib.base import TimeSeriesModel

class RandomForestModel(TimeSeriesModel):
    def __init__(self, n_estimators=100):
        self.model = RandomForestClassifier(n_estimators=n_estimators)

    def fit(self, X, y):
        self.model.fit(X, y.values.ravel())

    def predict(self, X):
        return self.model.predict(X)
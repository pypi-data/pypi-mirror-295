import numpy as np
from lib.base import Metric

class Accuracy(Metric):
    def calculate(self, actual, predicted):
        return np.mean(actual == predicted)
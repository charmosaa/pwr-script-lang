from abc import ABC, abstractmethod
import numpy as np
from time_series import TimeSeries

class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries):
        """Analyze the TimeSeries and return a list of anomaly messages."""
        pass

class OutlineDetector(SeriesValidator):
    """Detects outliers based on k times stddev"""
    def __init__(self, k):
        self.k = k

    def analyze(self, series):
        anomaly_messages = []
        mean = series.mean
        stddev = series.stddev
        
        # no valid data or all the same - no anomalies
        if mean is None or stddev is None or stddev == 0:
            return anomaly_messages
        
        for i, value in enumerate(series.values):
            # if value exists and its difference with mean is greater than k*stddev it's classified as an outlier
            if not np.isnan(value) and abs(mean - value) > self.k * stddev:
                anomaly_messages.append(f'Anomaly detected - value greater than {self.k * stddev} is an outlier of {value} on date: {series.dates[i]}')
        return anomaly_messages

class ZeroSpikeDetector(SeriesValidator):
    """Detects x or more consecutives zeros"""
    def __init__(self, min_zero=3):
        self.min_zero = min_zero

    def analyze(self, series):
        anomaly_messages = []
        zero_empty_count = 0

        for i, value in enumerate(series.values):
            if np.isnan(value) or value == 0:
                zero_empty_count += 1
            else:
                if zero_empty_count >= self.min_zero:
                    anomaly_messages.append(f'Anomaly detected: consecutive {zero_empty_count} zero or empty values from {series.dates[i-zero_empty_count]} to {series.dates[i-1]}')
                zero_empty_count = 0  # reset 
        
        if zero_empty_count >= self.min_zero:
            anomaly_messages.append(f'Anomaly detected: consecutive {zero_empty_count} zero or empty values from {series.dates[len(series.values)-zero_empty_count]} to {series.dates[len(series.values)-1]}')

        return anomaly_messages

class ThresholdDetector(SeriesValidator):
    """Detects values greater than threshold"""
    def __init__(self, threshold):
        self.threshold = threshold

    def analyze(self, series):
        anomaly_messages = []
        
        for i, value in enumerate(series.values):
            if not np.isnan(value) and value > self.threshold:
                anomaly_messages.append(f'Anomaly detected - value greater than {self.threshold}: {value} on date: {series.dates[i]}')
        return anomaly_messages


# duck typing example
class SimpleReporter:
    """Returns info about timesseries - is not a SeriesValidator (duck typing)"""
    def analyze(self, series: TimeSeries):
        return [f'Info: {series.measurement_name} at {series.station_code} has mean = {series.mean}']
from datetime import datetime, date
import numpy as np
from typing import List

class TimeSeries:
    def __init__ (self, measurement_name, station_code, frequency, dates: List[datetime], values: List, unit):
        # 'dates' and 'values' should be the same length
        if len(dates) != len(values):
            raise ValueError("Dates and values should have the same legth")
        
        self.measurement_name = measurement_name  
        self.station_code = station_code     
        self.frequency = frequency 
        self.dates = dates                    
        self.values = np.array(values, dtype=float) 
        self.unit = unit     

    def __str__(self):  
        return f"Time Series: measurement - {self.measurement_name}, station - {self.station_code}, frequency - {self.frequency}, unit - {self.unit}"

    def __getitem__ (self, key):
        if isinstance (key, int):
            return (self.dates[key], self.values[key])
        elif isinstance (key, slice):
            return list(zip(self.dates[key], self.values[key]))
        elif isinstance (key, datetime):
            if key in self.dates:
                return self.values[self.dates.index(key)]
            else:
                raise KeyError (f"No measurements for datetime: {key}")
        elif isinstance (key, date):
            result = [value for dt, value in zip(self.dates, self.values) if dt.date() == key]
            if not result:
                raise KeyError(f"No measurements for date: {key}")
            return result
        else:
            raise KeyError (f"Invalid key type: {type(key)}")
        
    @property
    def mean(self):
        """Return the mean of the available values, or None if no valid data."""
        if len(self.values) == 0 or np.all(np.isnan(self.values)):
            return None
        return np.nanmean(self.values)

    @property
    def stddev(self):
        """Return the standard deviation of the available values, or None if no valid data."""
        if len(self.values) == 0 or np.all(np.isnan(self.values)):
            return None
        return np.nanstd(self.values)
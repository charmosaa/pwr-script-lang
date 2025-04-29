import os
from time_series import TimeSeries
import pandas as pd
from series_validator import *

class Measurements: 
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.files = [f for f in os.listdir(self.dir_path) if f.endswith('.csv')] # gets csv files from directory
        self._loaded_series = []
        self._is_loaded = False

    def _load_time_series(self):
        if self._is_loaded:
            return
        for filename in self.files:
            filepath = os.path.join(self.dir_path, filename)
            
            # filename format: "2023_NO_1g.csv"
            parts = filename[:-4].split("_")
            if len(parts) != 3:
                print(f"Invalid filename: {filename}")
                continue  # skipping invalid 

            year, measurement, frequency = parts

            if len(measurement) > 8 and measurement[0].isupper() and measurement.isalpha():  # all the different weird filenames like PrekursoryZielonka and Depozycja
                print(f"Invalid filename: {filename}")
                continue 

            df = pd.read_csv(filepath, skiprows=6) # dates and values
           
            with open(filepath, 'r') as f:
                lines = [next(f) for _ in range(6)]  # first 6 lines - headers 

            station_codes = lines[1].strip().split(',')[1:] # they are separeted by , and we skip the row name
            units = lines[4].strip().split(',')[1:] # they are separeted by , and we skip the row name
            
            df.columns =  ['Date'] + station_codes # adding column names to dates + value table

            for i,code in enumerate(station_codes):
                time_series = TimeSeries (
                    measurement,
                    code,
                    frequency,
                    df['Date'],
                    df[code],
                    units[i]
                )
                self._loaded_series.append(time_series)
            self._is_loaded = True

    def __len__(self):
        self._load_time_series()
        return len(self._loaded_series)
    
    def __contains__(self, parameter_name: str):
        self._load_time_series()
        return any(ts.measurement_name.lower() == parameter_name.lower() for ts in self._loaded_series)

    def get_by_parameter(self, param_name: str):
        self._load_time_series()
        return [ts for ts in self._loaded_series if ts.measurement_name.lower() == param_name.lower()]

    def get_by_station(self, station_code: str) -> list[TimeSeries]:
        self._load_time_series()
        return [ts for ts in self._loaded_series if ts.station_code == station_code]

    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False):
        if preload:
            self._is_loaded = False
            self._load_time_series

        anomalies_dict = {}
        for ts in self._loaded_series:
            key = (ts.measurement_name, ts.station_code, ts.frequency, ts.unit)  # timeseries info as dictionary key
            for validator in validators:
                for msg in validator.analyze(ts):
                    if key not in anomalies_dict:
                        anomalies_dict[key] = []
                    
                    anomalies_dict[key].append(msg)     # for each timeseries we add all the anomaly messages to dict

        return anomalies_dict
                    

if __name__ == '__main__':
    # test / usage example
    measurements = Measurements('data/measurements')
    print(len(measurements))

    for ts in measurements.get_by_station('ZpSwinMatejkMOB'):
        print(ts)

    # task 7 + 8 - validators on all the timeseries
    validators = [OutlineDetector(k=3), ZeroSpikeDetector(min_zero=3) , ThresholdDetector(threshold=80), SimpleReporter()]

    anomalies_dict = measurements.detect_all_anomalies(validators)

    # printing results
    for key, messages in anomalies_dict.items():
        print(f"Anomalies for TimeSeries: {key})")
        for msg in messages:
            print(f"  - {msg}")
        print()  


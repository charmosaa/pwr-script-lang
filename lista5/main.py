import argparse
import random
from datetime import datetime
import numpy as np
import csv_parser
from pathlib import Path
import logging
import sys

# logger settings
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# DEBUG, INFO, WARNING → stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

# ERROR, CRITICAL → stderr
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)

# format
formatter = logging.Formatter('%(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)


# data 
stations = csv_parser.parse_meta(Path('data/stacje.csv'))
measurements_paths = csv_parser.group_measurement_files_by_key(Path('data/measurements'))

def get_random_station(measurement, frequency, start_date, end_date):
    """returns random station that was working between those dates and measured the value"""

    measurement_data = csv_parser.parse_measurment(measurements_paths[("2023", measurement, frequency)]) 

    stations_dict = measurement_data[0]
    
    # get all codes of the stations that measured this
    station_codes = [v for k, v in stations_dict.items() if k != 'Nr']
    
    # filter stations that were measuring this variable and were working between start and end dates
    filtered_stations = [
        station for station in stations 
        if (station['kod_stacji'] in station_codes and 
            parse_date(station['data_uruchomienia']) and 
            parse_date(station['data_zamkniecia']) and 
            parse_date(station['data_uruchomienia']) <= end_date and 
            parse_date(station['data_zamkniecia']) >= start_date)
    ]
    
    if filtered_stations:
        return random.choice(filtered_stations)
    else:
        return None
    
def stats_for_station(file_path, station_key, start_date, end_date):
    logger.info(f"opening file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            logger.info(f"closing file: {file_path}")
    except FileNotFoundError:
        logger.error(f"file not found: {file_path}")
        return None, None

    data_lines = lines[6:]
    values = []

    for line in data_lines:
        logger.debug(f"read {len(line.encode('utf-8'))} bytes")
        parts = line.strip().split(',')
        try:
            date = datetime.strptime(parts[0].strip(), '%m/%d/%y %H:%M')
        except ValueError:
            continue    #ignorring incorrect dates

        if date < start_date:
            continue
        if date > end_date:
            break

        try:
            value = float(parts[int(station_key) + 1])
            values.append(value)
        except (ValueError, IndexError):
            continue    # ignorring incorrect formats

    if values:
        mean = np.mean(values)
        std_dev = np.std(values)
        return mean, std_dev
    else:
        return None, None



def calculate_statistics(station_code, measurement, frequency, start_date, end_date):
    """returns mean and standard deviation for measurment in timerange for station_id"""
    
    measurement_data = csv_parser.parse_measurment(measurements_paths[(str(start_date.year), measurement, frequency)]) 

    # first row with numbers and codes
    stations_dict = measurement_data[0]
        
    # dict code to its key so we can read the values from the rows
    code_to_key = {v: k for k, v in stations_dict.items() if k != 'Nr'}

    if station_code not in code_to_key:
        return None, None

    station_key = code_to_key[station_code]

    return stats_for_station(measurements_paths[(str(start_date.year), measurement, frequency)], code_to_key[station_code],start_date, end_date)

    with open(measurements_paths[(str(start_date.year), measurement, frequency)], 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # first - 5 headers
    data_lines = lines[6:]

    # values from range of this station
    values = []

    for line in data_lines:
        parts = line.strip().split(',')
        date = datetime.strptime(parts[0].strip(), '%m/%d/%y %H:%M')

        if date < start_date:
            continue
        if date > end_date:
            break

        try:
            value = float(parts[int(station_key) + 1])
            values.append(value)
        except (ValueError, IndexError):
            continue  # skip rows with missing or bad data
            
    # calculate statistics if we have data
    if values:
        mean = np.mean(values)
        std_dev = np.std(values)
        return mean, std_dev
    else:
        return None, None
    
    


def parse_date(date_str):
    """Funkcja pomocnicza do parsowania daty z formatu rrrr-mm-dd"""
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d')
    return None

def create_parser():
    parser = argparse.ArgumentParser(description="CLI do przetwarzania danych stacji pomiarowych.")
    
    # main options
    parser.add_argument('measurment', type=str, help="Wielkość mierzona (np. PM10, PM2.5, NO, CO, ...)")
    parser.add_argument('freq', type=str, help="Częstotliwość pomiarów (np. 1g, 24g, ...)")
    parser.add_argument('start_date', type=str, help="Data początkowa w formacie rrrr-mm-dd")
    parser.add_argument('end_date', type=str, help="Data końcowa w formacie rrrr-mm-dd")
    
    subparsers = parser.add_subparsers(dest="command")
    
    # subcommand - random station
    random_station_parser = subparsers.add_parser('random_station', help="Wypisz losową stację spełniającą kryteria")
    
    # subcommand -avg and standard deviation for station_id
    statistics_parser = subparsers.add_parser('statistics', help="Oblicz średnią i odchylenie standardowe dla stacji")
    statistics_parser.add_argument('station_id', type=str, help="ID stacji do obliczeń")
    
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    # parse strings to dates
    start_date = parse_date(args.start_date)
    end_date = parse_date(args.end_date)
    
    # execution for random station
    if args.command == 'random_station':
        station = get_random_station(args.measurment, args.freq, start_date, end_date)
        if station:
            print(f"Losowa stacja: {station}")
        else:
            print("Brak stacji spełniających kryteria.")
    
    # exe for statistics
    elif args.command == 'statistics':
        mean, std_dev = calculate_statistics(args.station_id, args.measurment, args.freq, start_date, end_date)
        if mean is not None:
            print(f"Średnia: {mean:.2f}, Odchylenie standardowe: {std_dev:.2f}")
        else:
            print("Brak danych pomiarowych dla podanych kryteriów.")

if __name__ == '__main__':
    main()
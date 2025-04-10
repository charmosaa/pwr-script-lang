import re
import csv_parser
from pathlib import Path
import unidecode

def extract_dates(path: Path):
    date_pattern = r'\d{4}-\d{2}-\d{2}' # RRRR-MM-DD
    dates = []
    
    for station in csv_parser.parse_meta(path):
        start_date = station['data_uruchomienia']
        end_date = station['data_zamkniecia']
        
        if start_date:
            if re.match(date_pattern, start_date):
                dates.append(start_date)
        if end_date:
            if re.match(date_pattern, end_date):
                dates.append(end_date)

    return dates

def extraxt_geo(path: Path):
    geo_pattern = r'\d{1,3}\.\d{6}' # 1 to 3 digits followed by . and 6 digits

    coordinates = []

    for station in csv_parser.parse_meta(path):
        lat = station['szerokosc_geograficzna']
        lon = station['dlugosc_geograficzna']
        
        if lat and re.match(geo_pattern, str(lat)):
            coordinates.append(lat)
        if lon and re.match(geo_pattern, str(lon)):
            coordinates.append(lon)

    return coordinates

def extract_two_part_stations(path: Path):
    pattern = r'.+-.+' # name1-name2

    stations = []

    for station in csv_parser.parse_meta(path):
        if re.match(pattern, str(station['nazwa_stacji'])):
            stations.append(station['nazwa_stacji'])

    return stations

def rename(path: Path):
    stations = csv_parser.parse_meta(path)

    for station in stations:
        name = station['nazwa_stacji']
        name = re.sub(r' ', '_', name)   # replacing spaces with underscore
        name = unidecode.unidecode(name)    # decoding polish letters 
        station['nazwa_stacji'] = name

    return stations

def check_mob(path: Path):
    """ checks if code ends with MOB and kind is mobilna
        returns a list of incorrect stations (where code ends with MOB but kind is different) 
    """
    stations = csv_parser.parse_meta(path)

    incorrect_stations = []

    for station in stations:
        if re.search(r'MOB$', station['kod_stacji']): # if ends with MOB
            if station['rodzaj_stacji'] != 'mobilna':
                incorrect_stations.append(station) # if not mobilna it's incorrect - part of the result

    return incorrect_stations


def extract_three_part_locations(path: Path):
    pattern = r'.+-.+-.+' # name1-name2-name3

    locations = []

    for station in csv_parser.parse_meta(path):
        if re.match(pattern, str(station['adres'])): # idk if it's supposed to be adres or nazwa_stacji
            locations.append(station['adres'])

    return locations

def extract_comma_street_locations(path: Path):
    pattern = r'.*,.*(ul\.|al\.).*' # *, ul./al. *

    locations = []

    for station in csv_parser.parse_meta(path):
        if re.match(pattern, str(station['nazwa_stacji'])):
            locations.append(station['nazwa_stacji'])

    return locations

location_pattern = r'.*(ul\.|al\.).*,.*'
    

if __name__ == "__main__":
    data = extract_comma_street_locations(Path('data/stacje.csv'))
    
    for d in data:
        print(d)
    print(len(data))
    


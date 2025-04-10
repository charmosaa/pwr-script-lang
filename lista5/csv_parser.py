import csv
from datetime import datetime
from pathlib import Path
import re

def parse_meta(file_path: Path):
    """
    parse data in format:

        Nr,Kod stacji,Kod międzynarodowy,Nazwa stacji,"Stary Kod stacji (o ile inny od aktualnego)",
        Data uruchomienia,Data zamknięcia,Typ stacji,Typ obszaru,Rodzaj stacji,Województwo,
        Miejscowość,Adres,WGS84 φ N,WGS84 λ E

    to list of dicts 
    """
    stations = []
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        
        for row in reader:
            station = {
                'nr': int(row['Nr']),
                'kod_stacji': row['Kod stacji'],
                'kod_miedzynarodowy': row['Kod międzynarodowy'] or None,
                'nazwa_stacji': row['Nazwa stacji'],
                'stary_kod': row['Stary Kod stacji (o ile inny od aktualnego)'] or None,
                'data_uruchomienia': row['Data uruchomienia'],
                'data_zamkniecia': row['Data zamknięcia'],
                'typ_stacji': row['Typ stacji'],
                'typ_obszaru': row['Typ obszaru'],
                'rodzaj_stacji': row['Rodzaj stacji'],
                'wojewodztwo': row['Województwo'],
                'miejscowosc': row['Miejscowość'],
                'adres': row['Adres'] or None,
                'szerokosc_geograficzna': row['WGS84 φ N'],
                'dlugosc_geograficzna':  row['WGS84 λ E']
            }
            stations.append(station)
    
    return stations


def parse_measurment(file_path):

     with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        return [row for row in reader]


def group_measurement_files_by_key(path: Path):
    pattern = re.compile(r'(\d{4})_([A-Za-z0-9()]+)_([0-9a-zA-Z]+)\.csv')

    result = {}

    for file in path.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                key = tuple(match.groups())  # (rok, wielkość, częstotliwość)
                result[key] = file

    return result

if __name__ == "__main__":
    data = group_measurement_files_by_key(Path('data/measurements'))
    
    print(data)
    

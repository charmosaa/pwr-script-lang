from pathlib import Path
import csv_parser
import re

def get_addresses(path: Path, city):
    stations = csv_parser.parse_meta(path)

    city_stations = [station for station in stations if station['miejscowosc'] == city]

    city_stations_addresses = []

    for station in city_stations:
        street, number = parse_address(station['adres']) 
        city_stations_addresses.append((station['wojewodztwo'], city, street, number))

    return city_stations_addresses

def parse_address(address):
    address_parts = address.split()
    number_pattern = re.compile(r'^\d.*$')


    if number_pattern.match(address_parts[-1]):
        street_name = ' '.join(address_parts[:-1])
        number = address_parts[-1]
        return street_name, number
    else:
        return address, None
    

if __name__ == "__main__":
    print(get_addresses(Path('data/stacje.csv') ,'Wrocław'))
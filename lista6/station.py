class Station:
    def __init__(self, number, station_code, international_code, station_name, old_station_code, start_date, end_date, station_type, area_type, facility_type, voivodeship, city, address, latitude, longitude):
        self.number = int(number)
        self.station_code = station_code
        self.international_code = international_code
        self.station_name = station_name
        self.old_station_code = old_station_code
        self.start_date = start_date
        self.end_date = end_date
        self.station_type = station_type
        self.area_type = area_type
        self.facility_type = facility_type
        self.voivodeship = voivodeship
        self.city = city
        self.address = address
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __str__(self):
        return f"Station {self.station_code} '{self.station_name}' in {self.city}"

    def __repr__(self):
        return (f"Station(number={self.number}, station_code='{self.station_code}', "
                f"international_code='{self.international_code}', station_name='{self.station_name}', "
                f"old_station_code='{self.old_station_code}', start_date='{self.start_date}', "
                f"end_date='{self.end_date}', station_type='{self.station_type}', "
                f"area_type='{self.area_type}', facility_type='{self.facility_type}', "
                f"voivodeship='{self.voivodeship}', city='{self.city}', "
                f"address='{self.address}', latitude={self.latitude}, longitude={self.longitude})")

    def __eq__(self, other):
        if not isinstance(other, Station):
            return False
        return self.station_code == other.station_code


if __name__ == '__main__':
    # test / example usage
    s = Station(
        number=1,
        station_code="DsBialka",
        international_code="",
        station_name="Białka",
        old_station_code="",
        start_date="1990-01-03",
        end_date="2005-12-31",
        station_type="przemysłowa",
        area_type="podmiejski",
        facility_type="kontenerowa stacjonarna",
        voivodeship="DOLNOŚLĄSKIE",
        city="Białka",
        address="",
        latitude="51.197783",
        longitude="16.117390"
    )

    print(s)
    print(repr(s))

    s1 = Station(1, "DsBialka", "", "Białka", "", "1990-01-03", "2005-12-31", "przemysłowa", "podmiejski", "kontenerowa stacjonarna","DOLNOŚLĄSKIE", "Białka", "", "51.197783", "16.117390")

    s2 = Station(2, "DsBialka", "", "Białka - Nowa", "", "1995-01-01", "", "przemysłowa", "podmiejski", "kontenerowa stacjonarna", "DOLNOŚLĄSKIE", "Białka", "", "51.197783", "16.117390")

    print(s1 == s2)  


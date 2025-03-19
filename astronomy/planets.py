from skyfield.api import load

# Create a timescale and ask the current time.
ts = load.timescale()
t = ts.now()

# Load the JPL ephemeris DE421 (covers 1900-2050).
planets = load('de421.bsp')
earth, venus = planets['earth'], planets['venus']

# What's the position of Venus, viewed from Earth?
astrometric = earth.at(t).observe(venus)
ra, dec, distance = astrometric.radec()

print(ra)
print(dec)
print(distance)
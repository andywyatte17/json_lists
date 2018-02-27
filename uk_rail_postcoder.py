import csv

c1 = csv.reader(open('uk_rail_stations_2011-12_filtered.csv', 'rb'))
c2 = csv.writer(open('uk_rail_stations_2011-12_filtered_2.csv', 'wb'))

from geopy.geocoders import Nominatim # python -m pip install --user geopy

def postcodeToGeo(x):
    geolocator = Nominatim()
    location = geolocator.geocode(x)
    return "{},{}".format(location.longitude, location.latitude)

row = 0
for x in c1:
    row += 1
    long_lati = "long_lati"
    if row>1:
        try:
            long_lati = x[2]
            if x[2]=="?":
                result = postcodeToGeo(x[3])
                long_lati = result
                print(result, row)
        except:
            long_lati = "?"
    x[2] = long_lati
    c2.writerow(x)

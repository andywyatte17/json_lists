from __future__ import print_function
import csv
from sqlitedict import SqliteDict
from geopy.geocoders import Nominatim # python -m pip install --user geopy

with open('uk_rail_stations_2011-12_filtered.csv', 'rb') as fIn:
    with open('uk_rail_stations_2011-12_filtered_tmp.csv', 'wb') as fOut:
        fOut.write( fIn.read() )

c1 = csv.reader(open('uk_rail_stations_2011-12_filtered_tmp.csv', 'rb'))
c2 = csv.writer(open('uk_rail_stations_2011-12_filtered.csv', 'wb'))

urlcache = SqliteDict('./.uk_rail_postcoder_cache.sqlite', autocommit=True)

# ...

def postcodeToGeo(postcode):
    global urlcache
    try:
        return urlcache[postcode]
    except:
        pass
    geolocator = Nominatim()
    location = geolocator.geocode(postcode)
    s = "{},{}".format(location.longitude, location.latitude)
    urlcache[postcode] = s
    return s

# ...

def main():
    fast_finish = False
    row = 0
    for x in c1:
        row += 1
        long_lati = "long_lati"
        if row>1:
            if fast_finish:
                c2.writerow(x)
            else:
                try:
                    long_lati = x[2]
                    if x[2]=="?":
                        print("Getting {}... ".format(x), end='')
                        result = postcodeToGeo(x[3])
                        long_lati = result
                        print("{} {}".format(result, row))
                except KeyboardInterrupt:
                    fast_finish = True
                except:
                    long_lati = "?"
                x[2] = long_lati
                c2.writerow(x)

main()

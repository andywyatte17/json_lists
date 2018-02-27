import csv

c1 = csv.reader(open('uk_rail_stations_2011-12_filtered.csv', 'rb'))
c2 = csv.writer(open('uk_rail_stations_2011-12_filtered_2.csv', 'wb'))

import re
from postcodes import PostCoder
pc = PostCoder()

def filter_postcode(x):
    m = re.match(r'([A-Z]+[0-9]+) ([0-9]+[A-Z]+)', x)
    x = m.group(1) + ' ' + m.group(2)
    return x
    
row = 0
for x in c1:
    row += 1
    long_lati = "long_lati"
    if row>1:
        try:
            # result = pc.get(filter_postcode(x[3]))
            #lat = result['geo']['lat']
            #lng = result['geo']['lng']
            #long_lati = lng + "," + lat 
            long_lati = "filter_postcode(x[3])"
        except:
            long_lati = "?"
    c2.writerow(x)

import json
import csv
csv_r = csv.reader(open('uk_rail_stations_2011-12_filtered.csv', 'r'))
csv_w = csv.writer(open("umap-uk-rail-stations.csv", "w"))
csv_w.writerow(["lat", "lon", "name"])
c = 0
for x in csv_r:
    c+=1
    if c==1: continue
    if x[2]=='?': continue
    tmp = x[2]
    tmp = tmp.split(',')
    csv_w.writerow([tmp[1], tmp[0], x[4]])

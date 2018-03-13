import json
import csv
csv_w = csv.writer(open("umap-uk-parkdean-resorts.csv", "w"))
j = json.loads(open("parkdean-locations-filtered.json", "r").read())
csv_w.writerow(["lat", "lon", "name"])
for x in j:
    csv_w.writerow([x["Latitude"], x["Longitude"], x["ParkName"]])
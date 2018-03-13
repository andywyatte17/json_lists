from bs4 import BeautifulSoup
from sqlitedict import SqliteDict
import urllib2
import re
import csv

urlcache = SqliteDict('./.haven_url_cache.sqlite', autocommit=True)

POSTCODE_RGX = re.compile(R"([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z]))))\s?[0-9][A-Za-z]{2})")

def GetUrl(some_url):
    global urlcache
    try:
        return urlcache[some_url]
    except:
        pass
    import urllib
    r = urllib.urlopen(some_url).read()
    urlcache[some_url] = r
    return r

def FindPostcode(some_url):
    data = GetUrl(some_url)
    soup = BeautifulSoup(data, "lxml")
    for x in soup.find_all("div", class_="parkSecMain"):
        s = x.get_text("  ").encode("ascii", "ignore")
        m = POSTCODE_RGX.search(s)
        if m:
            return m.group(0)
    return "???"

soup = BeautifulSoup(open('haven.html', 'r').read(), "lxml")

def postcodeToGeo_lon_lat(postcode):
    global urlcache
    try:
        return urlcache[postcode]
    except:
        pass
    from geopy.geocoders import Nominatim # python -m pip install --user geopy
    geolocator = Nominatim()
    location = geolocator.geocode(postcode)
    lon_lat = (location.longitude, location.latitude)
    urlcache[postcode] = lon_lat
    return lon_lat

# https://www.haven.com/parks/

csv_w = csv.writer(open("umap-haven.csv", 'w'))
csv_w.writerow(["name", "postcode", "lon", "lat"])
for anchor in soup.find_all("a"):
    href = anchor["href"].replace("/parks/", "https://www.haven.com/parks/")
    title = anchor["title"]
    if not ("touring-camping" in href):
        postcode = FindPostcode(href)
        lon, lat = postcodeToGeo_lon_lat(postcode)
        csv_w.writerow([title.encode("ascii", "ignore"), postcode, lon, lat])
        
urlcache.close()

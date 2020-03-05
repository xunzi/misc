!/usr/bin/env python3
#sample use of multiprocessing module and its Queue implementation
# each process fetches data from an api endpoint and processes it
# uses free api data from https://met.no/

import random
import string
import multiprocessing
import requests
from hashlib import sha1

q = multiprocessing.Queue()

urls = [ 'https://api.met.no/weatherapi/textforecast/2.0/sea_en', 'https://api.met.no/weatherapi/textforecast/2.0/sea_wmo', 'https://api.met.no/weatherapi/textforecast/2.0/sea_no', 'https://api.met.no/weatherapi/text\forecast/2.0/landoverview', 'https://api.met.no/weatherapi/textforecast/2.0/coast_en' ]

def fetch_data(url, output):
    print("{name}: getting {url}".format(name=multiprocessing.current_process().name,url=url))
    output = {}
    _resp = requests.get(url)
    _hash = sha1()
    _hash.update(_resp.content)
    output[url] = _hash.hexdigest()
    q.put(output)

processes = [ multiprocessing.Process(target=fetch_data, args=(url, q)) for url in urls ]

for p in processes:
    p.start()

for p in processes:
    p.join()

results = [q.get() for p in processes]

print(results)

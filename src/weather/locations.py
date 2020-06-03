from bs4 import BeautifulSoup

import pycurl
from io import BytesIO, StringIO
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

locations = pd.read_csv("locations.csv",index_col="airport")

def get_location(location):
    buffer = BytesIO()
    c = pycurl.Curl()
    url = {
        "K":"https://www.airnav.com/airport/",
        "C":"https://skyvector.com/airport/",
        }
    c.setopt(c.URL, f'{url[location[0]]}{location}')
    c.setopt(c.WRITEDATA, buffer)
    body = c.perform_rs()
    c.close()
    return body

# print(locations)

for location in locations.index:
    print(location)
    html = get_location(location)
    if html:
        soup = BeautifulSoup(html,"html.parser")
        print(soup.table)
        quit()

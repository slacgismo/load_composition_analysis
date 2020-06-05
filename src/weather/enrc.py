import sys, os
from datetime import datetime, timedelta
import pytz
import pycurl
from io import BytesIO, StringIO
import pandas as pd
import numpy as np

def find_csvfile(name):
    return str(sys.modules[__name__].__file__).replace(f"/enrc.py",f"/{name}")

def to_float(x):
    try:
        return float(x.rstrip('s'))
    except:
        return float("nan")

def to_dict(d):
    try:
        return eval(d)
    except:
        return {}

def to_localhour(t):
    global my_tzinfo
    return my_tzinfo.localize(datetime.fromisoformat(t[0:13] + ":00:00"),is_dst=False)

def to_float(x):
    try:
        return float(x.rstrip('s'))
    except:
        return float("nan")
locations = pd.read_csv(find_csvfile("locations.csv"),converters={
        "location":str,
        "airport":str,
        "source":str,
        "city":str,
        "station":to_dict,
        "zipcode":str,
        "latitude":to_float,
        "longitude":to_float,
        "elevation":to_float,
        "timezone":str,
        "tzoffset":int,
        "dst":int,
    }).set_index("location")

station_list = locations[locations["source"]=="ENRC"]["station"].to_dict()
timezones = locations[locations["source"]=="ENRC"]["timezone"].to_dict()

dtype = {
    'Date/Time':to_localhour,
    'Temp (°C)':to_float,
    'Rel Hum (%)':to_float,
}
columns = {
    "Date/Time": "localtime",
    "Temp (°C)" : "temperature",
    "Rel Hum (%)" : "humidity",
}
index = "localtime"

def heatindex(data,tname,rhname):
    T = data[tname]*9./5.+32.
    RH = data[rhname]
    try:
        if T < 80.0 :
            HI = 0.75*T + 0.25*( 61.0+1.2*(T-68.0)+0.094*RH)
        else :
            HI = -42.379 + 2.04901523*T + 10.14333127*RH - 0.22475541*T*RH - 0.00683783*T*T - 0.05481717*RH*RH + 0.00122874*T*T*RH + 0.00085282*T*RH*RH - 0.00000199*T*T*RH*RH
            if RH < 13.0 and T < 112.0 :
                HI -= ((13.0-RH)/4.0)*sqrt((17.0-(T-95.0).abs())/17.0)
            elif RH > 85.0 and T < 87.0 :
                HI += ((RH-85.0)/10.0) * ((87.0-T)/5.0);
    except:
        HI = float("nan")
    return round(HI,1)

process = {
    "heatindex" : [heatindex,"temperature","humidity"]
}

UTC = pytz.timezone("UTC")
my_tzinfo = UTC

def get_tzinfo():
    global my_tzinfo
    return my_tzinfo

def set_tzinfo(timezone):
    global my_tzinfo
    my_tzinfo = pytz.timezone(timezone)

for key, value in station_list.items():
    saveas = f"enrc/{key}.csv"
    if os.path.exists(saveas): 
        data = pd.read_csv(saveas,
            converters = {
                "localtime": datetime.fromisoformat,
                "temperature": float,
                "humidity": float,
            }, 
            index_col = 0)
    else:
        set_tzinfo(timezones[key])
        blocks = []
        for station, years in value.items():
            print(f"{key}: {station}-",end='')
            for year in range(years[0],years[1]+1):
                print(str(year)[-1],end='')
                c = pycurl.Curl()
                for month in range(1,13):
                    buffer = BytesIO()
                    c.setopt(c.URL, f'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={station}&Year={year}&Month={month}&Day=1&timeframe=1&submit=Download+Data')
                    c.setopt(c.WRITEDATA, buffer)
                    body = c.perform_rs()
                    if c.getinfo(pycurl.HTTP_CODE) != 200:
                        print(f"\nERROR: no data for {station}/{year}-{month}.csv")
                        print(f"{key}: {station}/{year}",end='')
                    else:
                        df = pd.read_csv(StringIO(body),
                            usecols = columns.keys(),
                            converters = dtype)
                        df = df.filter(list(columns.keys()))
                        df = df.rename(
                            mapper=columns,
                            axis = "columns")
                        df.dropna(inplace=True)
                        df = df.set_index(index)
                        df.drop_duplicates(inplace=True)
                        if len(df) > 0:
                            for field,value in process.items():
                                if callable(value[2]):
                                    value[2] = value[2]()
                                df[field] = df.apply(lambda row: value[0](row,value[1],value[2]),axis=1)
                        blocks.append(df)
                    sys.stdout.flush()
                c.close()
            print(".")
        data = pd.concat(blocks,sort=True)
        data.to_csv(saveas)
    first = data.index.min()
    last = data.index.max()
    count = len(data.index)
    hours = (last-first).total_seconds()/3600.0
    print(f"{saveas}: {first} to {last}, {count} records, {hours-count:.0f} hours missing, {count/hours*100.0:.1f}% coverage")

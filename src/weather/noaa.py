#
# NOAA_WEATHER
#

import sys, os, glob
import pandas as pd
import datetime as dt
import numpy as np
import pytz

UTC = pytz.timezone("UTC")
my_tzinfo = UTC

def find_csvfile(name):
    return str(sys.modules[__name__].__file__).replace(f"/noaa.py",f"/{name}")

def set_tzinfo(timezone):
    global my_tzinfo
    my_tzinfo = pytz.timezone(timezone)

def get_tzinfo():
    global my_tzinfo
    return my_tzinfo

def to_localhour(t):
    global my_tzinfo
    return my_tzinfo.localize(dt.datetime.fromisoformat(t[0:13] + ":00:00"),is_dst=False)

def to_datetime(t):
    return dt.datetime.fromisoformat(t+"+00:00")

def to_timestamp(t):
    return to_datetime(t).timestamp()

def to_timestamp_hour(t):
    return int(round(to_timestamp(t)/3600))

def to_float(x):
    try:
        return float(x.rstrip('s'))
    except:
        return float("nan")

def heatindex(data,tname,rhname):
    T = data[tname]
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

def localtime(data,column,tzinfo):
    return dt.datetime.fromtimestamp(data[column]*3600).astimezone(tzinfo)

def utchour(data,column,modulo):
    return int(round(data[column].timestamp()/modulo))

def nop(msg):
    return

def collate_data(filespec, timezone,
        columns = {
            'DATE': 'localtime',
            'HourlyDryBulbTemperature': 'temperature',
            'HourlyRelativeHumidity': 'humidity',
            },
        dtype = {
            'DATE':to_localhour,
            'HourlyDryBulbTemperature':to_float,
            'HourlyRelativeHumidity':to_float,
        },
        process = {
            "heatindex" : [heatindex,"temperature","humidity"]
        },
        drop_duplicates = "localtime",
        returnas = pd.DataFrame,
        index = "localtime",
        progress=nop,
        saveas = None,
        refresh = 'never'):
    set_tzinfo(timezone)
    if saveas:
        csvsave = find_csvfile(saveas)
        if os.path.exists(csvsave) and refresh == 'never':
            return pd.read_csv(csvsave)
    csvlist = sorted(glob.glob(filespec))
    result = pd.DataFrame()
    for csvname in csvlist:
        progress(f"Reading {csvname}...")
        data = pd.read_csv(find_csvfile(csvname),
            usecols=columns.keys(),
            low_memory=True,
            converters=dtype)
        data = data.filter(list(columns.keys())).rename(
            mapper=columns,
            axis='columns')
        data.dropna(inplace=True)
        result = result.append(data)
    for key,value in process.items():
        progress(f"Computing {key}...")
        if callable(value[2]):
            value[2] = value[2]()
        result[key] = result.apply(lambda row: value[0](row,value[1],value[2]),axis=1)
    if drop_duplicates:
        progress(f"Dropping duplicate {drop_duplicates} records...")
        result.set_index(drop_duplicates)
        result.drop_duplicates(inplace=True)
    if index:
        progress(f"Indexing on {index}...")
        result.set_index(index,inplace=True)
    if saveas:
        progress(f"Saving to {csvsave}")
        result.to_csv(csvsave)
    progress("Processing complete")
    if returnas:
        return returnas(result)
    else:
        return None

def to_day(t):
    return int(dt.datetime.fromisoformat(t).timestamp()/86400)

def extract_daily_minmax(filespec,
        location = None,
        percentiles = [0.1,0.9],
        column = "heatindex",
        localtime = "localtime",
        progress = nop):
    result = pd.DataFrame()
    progress(f"Reading {filespec}...")
    data = pd.read_csv(find_csvfile(filespec),converters={localtime:to_day}).rename(mapper={localtime:"day"},axis="columns")
    result = pd.DataFrame()
    days = data.groupby(["day"])[column]
    result["min"] = days.min()
    result["max"] = days.max()
    result["minrank"] = result["min"].rank(pct=True)
    result["maxrank"] = result["max"].rank(pct=True)
    min = result[result["minrank"]>percentiles[0]]["min"].min()
    max = result[result["maxrank"]>percentiles[1]]["max"].max()
    values = {"min":min,"max":max}
    if location:
        return {location: values}
    else:
        return values

locations = pd.read_csv(find_csvfile("locations.csv"),converters={
        "location":str,
        "zipcode":str,
        "source":str,
        "latitude":to_float,
        "longitude":to_float,
        "elevation":to_float,
    }).set_index("location")

def get_location(location,info=None):
    global locations
    if info:
        return locations.loc[location][info]
    else:
        return {location: dict(locations.loc[location])}

if __name__ == '__main__':
    def show_progress(msg):
        print(msg)
        sys.stdout.flush()

    data = collate_data("noaa/PDX-*.csv","US/Pacific",
        saveas="noaa/PDX.csv",
        progress=show_progress,
        refresh='never')

    minmax = extract_daily_minmax("noaa/PDX.csv")
    print(f"PDX: {minmax}")

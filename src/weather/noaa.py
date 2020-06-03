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

def collate_data(location,
        filespec = 'auto',
        timezone = 'auto',
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
        saveas = 'auto',
        refresh = 'never'):
    """Collate NOAA LCD weather downloads

    Parameters:
        columns (dict) - specify NOAA LCD columns to map into collated data
        dtype (dict) - specify the data types for columns to collate
        process (dict) - specify post-processing functions and parameters
        drop_duplicates (str) - specify column index to drop duplicates on
        returnas (callable or class) - specify return data type
        progress (callable) - specify progress callback function
        saveas (str) - specify CSV file to save data (default is None)
        refresh (str) - specify when to refresh (default is 'never')
    Returns:
        varies - data processed by `convert` parameter
    """
    if filespec == 'auto':
        filespec = f"noaa/{location}-*.csv"
    if timezone == 'auto':
        timezone = get_location(location,"timezone")
    if saveas == 'auto':
        saveas = f"noaa/{location}.csv"
    set_tzinfo(timezone)
    if saveas:
        csvsave = find_csvfile(saveas)
        if os.path.exists(csvsave) and refresh == 'never':
            return pd.read_csv(csvsave)
    csvlist = sorted(glob.glob(filespec))
    result = []
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
        result.append(data)
    result = pd.concat(result)
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

def extract_daily_minmax(location,
        filespec = 'auto',
        percentiles = [0.1,0.9],
        column = "heatindex",
        localtime = "localtime",
        ):
    """Extract daily min/max temperature values

    Parameters:
        filespec (str) - file containing weather data
        percentiles (list) - min and max percentiles
        localtime (str) - column name specifying localtime

    Returns:
        dict = {"min": min-value, "max": max-value}
    """
    if filespec == 'auto':
        filespec = f"noaa/{location}.csv"
    result = pd.DataFrame()
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
    return values

locations = pd.read_csv(find_csvfile("locations.csv"),converters={
        "location":str,
        "airport":str,
        "source":str,
        "city":str,
        "zipcode":str,
        "latitude":to_float,
        "longitude":to_float,
        "elevation":to_float,
        "timezone":str,
        "tzoffset":int,
        "dst":int,
    }).set_index("location")

def get_location(location,info=None):
    """Get location information

    Parameters:
        location (str) - location code (e.g., "PDX")
        info (str) - column name (e.g., "city")

    Returns:
        dict - if 'info' is 'None'
        value - if 'info' is a valid column name
    """
    global locations
    if info:
        return locations.loc[location][info]
    else:
        return {location: dict(locations.loc[location])}

if __name__ == '__main__':
    def show_progress(msg):
        print(msg)
        sys.stdout.flush()

    collate_data("PDX",progress=show_progress)
    print(extract_daily_minmax("PDX"))

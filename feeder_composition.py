import pandas as pd
import numpy as np
import os
import datetime
from calendar import monthrange
import matplotlib.pyplot as plt

class config:
    eu_dict_ceus = dict(zip(
["heat_pump", "other_electric_heat", "cooling", "water_heating", "cooking"],
["Vent", "Heat", "Cool", "HotWater", "Cook"],
))

    enduse_dict = dict(zip(
["Heat", "Cool", "Vent", "HotWater", "Cook", "Refrig",
"ExtLight", "IntLight", "OffEquip", "Misc", "Process", "Motors", "AirComp"],
["Heating", "Cooling", "Vent", "WaterHeat", "Cooking", "Refrig",
"ExtLight", "IntLight", "OfficeEquip", "Misc", "Process", "Motors", "AirComp"],
))
    eu_dict_elec = dict(zip(
['heat_pump', "other_electric_heat", "cooling", "water_heating", "cooking"],
['hc', "heating", "cooling", "waterheat", "oven"]
))
    eu_dict = dict(zip(
["other_electric_heat", "cooling", "water_heating", "cooking"],
["Heat", "Cool", "HotWater", "Cook"]
))
    eu_dict_elec_ceus = dict(zip(
["Heat", "Cool", "HotWater", "Cook"],
["other_electric_heat", "cooling", "water_heating", "cooking"]
))
    res_comp_dict_ceus = dict(zip(
    ['Heat', 'Cool', 'HotWater',
       'Refrig', 'ExtLight', 'IntLight', 'Vent', 'Misc',
       'Cook', 'AirComp', 'Process', 'OffEquip', 'Motors'],
    ['heating', 'cooling', 'hotwater',
       'refrigeration', 'exterior_lights', 'interior_lights', 'ventilation', 'miscellaneous',
       'cooking', 'air_compressors', 'process', 'office_equipment', 'motors']

))
    res_comp_dict = dict(zip(
    ['heating', 'cooling', 'waterheat',
       'refrig', 'computer', 'dryer', 'entertainment', 'freezer',
       'lighting', 'other', 'oven', 'plug', 'washer'],
    ['heating', 'cooling', 'hotwater',
       'refrigeration', 'computer', 'dryer', 'entertainment', 'freezer',
       'lights', 'other', 'oven', 'plugs', 'washer']

))
    res_comp_dict_rbsa = dict(zip(
    ['heating', 'cooling', 'hotwater',
       'refrigeration', 'computer', 'dryer', 'entertainment', 'freezer',
       'lights', 'other', 'oven', 'plugs', 'washer'],
    ['heating', 'cooling', 'waterheat',
       'refrig', 'computer', 'dryer', 'entertainment', 'freezer',
       'lighting', 'other', 'oven', 'plug', 'washer']

))

    weather_enduses = {'sensitive': ['Cool', 'Heat'], 'insensitive': ['Process','Vent', 'AirComp', 'Refrig', 'Motors', 'OffEquip', 'Misc', 'ExtLight', 'Cook', 'HotWater', 'IntLight']}
    weather_enduses_rbsa = {'sensitive' : ['cooling', 'heating', 'other'], 'insensitive': ['computer', 'dryer', 'entertainment', 'freezer', 'lighting', 'oven', 'plug', 'refrig', 'washer', 'waterheat']}
    btype_dict = {'office': ['LOFF'], 'lodging': ['LODG'], 'commercial': ['AWHS', 'COLL', 'GROC', 'HLTH', 'MISC', 'REFW', 'REST', 'RETL', 'SCHL', 'WRHS', 'AOFF', 'SOFF'], 'residential' : ['RES']}
    region_df = pd.DataFrame({'state': ["ID", 'MT', 'OR', 'WA'], 'region': ["Mountain", "Mountain", "Pacific", 'Pacific'] })
    rbsa_locations = pd.merge(pd.read_csv('rbsa_locations.csv'), region_df, 'left', 'state')

def get_datetime(ts):
    return datetime.datetime.strptime(ts,"%d%b%y:%H:%M:%S")
def get_datetime_rbsa(ts):
    return datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
def noaa_datetime(ts):
    return datetime.datetime.strptime(ts,"%Y-%m-%d %H:%M:%S%z")

def get_datetime_ceus(ts):
    return datetime.datetime.strptime(ts,"%Y-%m-%d %H:%M:%S")

def read_files():
    siteid_df_dict = {}
    for csv in os.listdir("C:/Users/Palash Goiporia/GISMO_files/rbsa_data/data/rbsa_sites/") :
        if csv.endswith(".csv"):
            siteid_df_dict[csv.split('.')[0]] = pd.read_csv("C:/Users/Palash Goiporia/GISMO_files/rbsa_data/data/rbsa_sites/" + csv, converters={"time":get_datetime})
    return siteid_df_dict

def get_weather(siteid, years = [2012, 2013]):

    locations = pd.read_csv("C:/Users/Palash Goiporia/GISMO_files/rbsa_data/rbsa_locations.csv")
    locations['postcode'] = np.array(locations['postcode'])//100
    siteid_zip = {}
    for i in range(locations.shape[0]):
        siteid_zip[str(locations.iloc[i][0])] = locations.iloc[i][3]

    temp = pd.read_csv('C:/Users/Palash Goiporia/GISMO_files/rbsa_data/weather/%s.csv' %(siteid_zip[siteid]), low_memory = False, converters = {'DATE': get_datetime_rbsa}).fillna(0)
    temp['index'] = temp['DATE']
    temp = temp.set_index('index')
    temp = temp[(temp["REPORT_TYPE"] != "SOD  ") & (temp["REPORT_TYPE"] != "SOM  ")]
    #temp = temp.reset_index()
    temp = temp[["DATE","HourlyDryBulbTemperature"]]

    temp = temp[temp.index.year.isin(years)]
    temp['date_hour'] = [datetime.datetime(t.year, t.month, t.day, t.hour, 0, 0) for t in temp['DATE']]

    cleaned_temp = np.array([])
    for i in np.array(temp["HourlyDryBulbTemperature"]):
        try:
            if i != -100:
                cleaned_temp = np.append(cleaned_temp, int(i))
            else:
                cleaned_temp = np.append(cleaned_temp, cleaned_temp[-1:])

        except ValueError:
            cleaned_temp = np.append(cleaned_temp, cleaned_temp[-1:])
    temp["HourlyDryBulbTemperature"] = cleaned_temp
    temp = temp.groupby("date_hour").mean()
    temp["index"] = temp.index.values
    temp = temp.rename(columns = {"HourlyDryBulbTemperature": "temp"})

    return temp

def area(siteid):
    sqft = pd.read_csv('C:/Users/Palash Goiporia/GISMO_files/rbsa_data/SFMaster_housegeometry.csv')
    sqft = sqft[["siteid", "SummarySketchSqFt_Calculated"]]
    sqft = sqft[sqft["siteid"] == siteid].iloc[0][1]
    return sqft

from datetime import timedelta, date

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def get_keys(dictionary, val):
    for key, value in dictionary.items():
         if val in value:
            return key

    return "key doesn't exist"

def inverse_mapping(f):
    return f.__class__(map(reversed, f.items()))

#siteid = 10388
def rbsa_file_reader(weekday, electrification):

    #weekday = 'weekday'
#def rbsa_file_reader(weekday):
    if weekday == "weekday":
        weekday = 1
    elif weekday == "weekend":
        weekday = 2
    else:
        weekday = None
    area_dict = {}
    d_dict = {}
    load_dict = {}
    cleaned_df = None
    total_area = 0
    temp_df = None

    regional_electrification = {}
    for i in set(electrification["region"]):
        x = {}
        for j in ["commercial", "residential"]:
            x[j] = electrification[(electrification["region"] == i) & (electrification["building_type"] == j)].iloc[0][3:]
        regional_electrification[i] = x
    rbsa_dict = pd.read_csv("rbsa_data/rbsa-dict.csv").fillna('ignore')

    enduses = []
    for i in range(rbsa_dict.shape[0]):
        if (rbsa_dict["category"][i] == "Service"):
            enduses.append("ignore")
        elif rbsa_dict["eu"][i] == "HC":
            enduses.append("HeatCool")
        elif i in range(194, 204):
            enduses.append('IntLight')
        elif rbsa_dict["eu"][i] == "misc":
            enduses.append("Misc")
        elif rbsa_dict["eu"][i] == "Gas":
            enduses.append("ignore")
        else:
            enduses.append(rbsa_dict["eu"][i])
    rbsa_dict["eu"] = enduses
    for i in range(rbsa_dict.shape[0]):
        if rbsa_dict['Alt_enduses'][i] == 'ignore':
            if rbsa_dict['eu'][i] == 'IntLight' or rbsa_dict['eu'][i] == 'ExtLight':
                rbsa_dict['Alt_enduses'][i] = 'lighting'
            elif rbsa_dict['eu'][i] == 'Misc':
                rbsa_dict['Alt_enduses'][i] = 'other'
            elif rbsa_dict['eu'][i] == 'Appliances':
                rbsa_dict['Alt_enduses'][i] = 'plug'
            elif rbsa_dict['eu'][i] == 'Electronics':
                rbsa_dict['Alt_enduses'][i] = 'entertainment'
            elif rbsa_dict['category'][i] == 'Service':
                rbsa_dict['Alt_enduses'][i] = 'ignore'
            elif rbsa_dict["eu"][i] == "HeatCool" and rbsa_dict["category"][i] == "HVAC":
                rbsa_dict['Alt_enduses'][i] = 'hc'
            #elif rbsa_dict['eu'][i] == 'HeatCool':
                #rbsa_dict['Alt_enduses'][i] = 'cooling'
            else:
                rbsa_dict['Alt_enduses'][i] = rbsa_dict["eu"][i].lower()


    rbsa_dict = rbsa_dict[rbsa_dict['Alt_enduses'] != 'ignore']


    for file in ["rbsa_data/data/rbsa1-1.csv", "rbsa_data/data/rbsa1-2.csv", "rbsa_data/data/rbsa1-3.csv", "rbsa_data/data/rbsa1-4.csv"]:
        reader = pd.read_csv(file, low_memory = False, converters={"time":get_datetime})
        time = [datetime.datetime(t.year, t.month, t.day, t.hour, 0, 0) for t in reader["time"]]
        reader["time"] = time
        if weekday:
            reader["weekday"] = np.where(np.array([t.weekday() for t in time]) < 5, 1, 2)
            reader = reader[reader["weekday"] == weekday]
            reader = reader.drop(columns = ["weekday"])

        #rbsa_dict = pd.read_csv("rbsa-dict.csv")#.dropna()
        columns = list(reader.columns)[2:]
        column_prefixes = [i.split(' ')[0] for i in columns]
        enduses_df = pd.DataFrame({"column_prefixes": column_prefixes, "columns" : columns, "index" : np.arange(len(columns))})
        rbsa_dict_energy = rbsa_dict[rbsa_dict["units"] != "Hours"]
        rbsa_dict_energy = pd.merge(rbsa_dict, enduses_df, left_on = "enduse_code", right_on = "column_prefixes")
        #rbsa_dict_energy = rbsa_dict_energy.sort_values('index')

        enduse_map = {}
        category_map = {}
        for i in range(rbsa_dict_energy.shape[0]):
            try:
                enduse_map[rbsa_dict_energy['Alt_enduses'][i]].append(rbsa_dict_energy['columns'][i])
            except:
                enduse_map[rbsa_dict_energy['Alt_enduses'][i]] = []
                enduse_map[rbsa_dict_energy['Alt_enduses'][i]].append(rbsa_dict_energy['columns'][i])
            try:
                category_map[rbsa_dict_energy['category'][i]].append(rbsa_dict_energy['columns'][i])
            except:
                category_map[rbsa_dict_energy['category'][i]] = []
                category_map[rbsa_dict_energy['category'][i]].append(rbsa_dict_energy['columns'][i])
            #reader = reader[reader["siteid"] == siteid]
        time = reader["time"]
        sites = reader["siteid"]
        reader = reader[rbsa_dict_energy["columns"]]
        reader["time"] = time
        reader["siteid"] = sites




        for siteid in set(reader["siteid"]):
            reader_test = reader[reader["siteid"] == siteid]
            reader_test_area = reader[reader["siteid"] == siteid].fillna(-10)

            reader_test = reader_test.groupby("time").sum()
            reader_test_area = reader_test_area.groupby("time").sum()
            d=None

            if temp_df is not None:
                try:
                    temp_df = temp_df.append(get_weather(str(siteid)))
                except FileNotFoundError:
                    print("Weather file doesn't exist for station " + str(siteid))
            else:
                try:
                    temp_df = get_weather(str(siteid))
                except FileNotFoundError:
                    print("Weather file doesn't exist for station " + str(siteid))

            for eu,cols in enduse_map.items():
                if eu != "ignore":
                    col_new = cols
                    #col_new.append("index")
                    cd = reader_test_area[cols]
                    index = np.array(reader_test_area.index.values)
                    #cd["time"] = index
                    #pd.merge(cd, temp1, left_on = cd.index, right_on = 'index')
                    ct = cd.shape[1]
                    yy = pd.DataFrame({"sites":cd.count(axis=1),eu:cd.sum(axis=1)})
                    if max(np.array(yy[eu])[1:]) == -40*ct :
                        try:
                            area_dict[eu] += 0
                        except:
                            area_dict[eu] = 0
                    else:
                        try:
                            area_dict[eu] += area(siteid)
                        except:
                            area_dict[eu] = area(siteid)
                    cd = reader_test[cols]
                    index = np.array(reader_test.index.values)
                    yy = pd.DataFrame({"sites":cd.count(axis=1),eu:cd.sum(axis=1)})
                    if d is None :
                        d = yy
                    else:
                        d.insert(len(d.columns),eu,yy[eu])
            d["time"] = d.index.values

            total_area = total_area + area(siteid)
            for col in electrification.columns[3:]:
                x = np.array(d[config.eu_dict_elec[col]])
                d[config.eu_dict_elec[col]] = x/regional_electrification[config.rbsa_locations[config.rbsa_locations['siteid'] == siteid].iloc[0][-1]]["residential"][list(electrification.columns[3:]).index(col)]

            d_dict[siteid] = d
            try:
                cleaned_df = cleaned_df.append(d)
            except:
                cleaned_df = d

            print("siteid " + str(siteid) + " processed")

    temp_2012 = temp_df.groupby('index').mean().iloc[:8760, :]
    cleaned_df = cleaned_df.rename(columns = {"time": "date_time"})
    cleaned_df = cleaned_df.groupby('date_time').sum()

    for col in cleaned_df.columns[1:]:
        cleaned_df[col] = np.array(cleaned_df[col])/area_dict[col]
        load_dict[col] = pd.merge(cleaned_df[[col]], temp_2012, left_index = True, right_index = True)#.drop(columns = ["index"])



    load_df = pd.DataFrame({"power":cleaned_df.iloc[: ,1:].sum(axis=1)})




    load_test = pd.merge(load_df, temp_2012, left_index = True, right_index = True)

    #print('Processed ' + str(siteid))

    return [load_test, load_dict, area_dict, total_area]

def composite_enduse(filename, electrification, building = 'commercial'):
    components_df = pd.read_csv('C:/Users/Palash Goiporia/GISMO_files/load_composition_analysis/src/enduse/components-latest.csv')
    if building == 'commercial':
        components_df = components_df.iloc[:7].dropna(axis = 1)
        zone, build = filename.split('_')

    A = components_df.iloc[:, 2:].to_numpy()

    regional_electrification = {}
    for i in set(electrification["region"]):
        x = {}
        for j in ["commercial", "residential"]:
            x[j] = electrification[(electrification["region"] == i) & (electrification["building_type"] == j)].iloc[0][3:]
        regional_electrification[i] = x


    area_dict = {}

    ceus_df = pd.read_excel('C:/Users/Palash Goiporia/GISMO_files/ceus_data/xls/%s.xls' %(filename), sheet_name = 'expEndUse8760')

    hourly_load = {}
    for fuel in ['Elec']:
        fuel_load = {}
        df = ceus_df[ceus_df["Fuel"] == fuel]
        for eu in set(ceus_df["EndUse"]):
            load = []
            d = df[df["EndUse"] == eu]
            for i in range(d.shape[0]):
                load.append(np.array(d.iloc[i, 5:]))
            fuel_load[eu] = load
            #for col in ceus_df.columns[5:]:
             #   load_dict[int(col[4:])%24] = np.array(df[col])
            #fuel_load[eu] = load_dict
        hourly_load[fuel] = fuel_load

    months = np.array([])
    days = np.array([])
    hours = np.array([])
    for month in range(1,13):
        months = np.append(months, np.array([[int(month) for i in range(24)] for j in range(monthrange(2002, month)[1])]).flatten())
        days = np.append(days, np.array([[int(j+1) for i in range(24)] for j in range(monthrange(2002, month)[1])]).flatten())
        hours = np.append(hours, np.array([[int(i) for i in range(24)] for j in range(monthrange(2002, month)[1])]).flatten())

    df = pd.DataFrame({'Mth': months, 'Dy': days, 'Hr': hours})
    for eu in hourly_load["Elec"].keys():
        df[eu] = np.array([hourly_load["Elec"][eu][i] for i in range(len(hourly_load["Elec"][eu]))]).flatten()

    for col in electrification.columns[4:]:
        x = np.array(df[config.eu_dict[col]])
        df[config.eu_dict[col]] = x/regional_electrification['Pacific'][building][list(electrification.columns[4:]).index(col)]

    df.insert(0, 'Date', [datetime.datetime(2002, int(df["Mth"][t]), int(df["Dy"][t]), int(df["Hr"][t])) for t in range(df.shape[0])])
    df = pd.merge(df, pd.read_csv('C:/Users/Palash Goiporia/GISMO_files/ceus_data/weather/%s.csv' %(zone), converters = {'hour': get_datetime_ceus}), left_on = 'Date', right_on = 'hour')

    sqft_df = pd.read_excel('C:/Users/Palash Goiporia/GISMO_files/ceus_data/xls/%s.xls' %(filename), sheet_name = 'expSqFt')
    #sqft_df
    for col in df.columns[4:-2]:
        area_dict[col] = sqft_df[sqft_df["SegID"] == config.enduse_dict[col]].iloc[0][1]
      #  if area == 0:
            #df[col] = np.array(df[col])*area
        #else:
         #   df[col] = np.array(df[col])/area


    components = np.array(components_df['component'])
    common_enduse_df = pd.DataFrame(columns = components)
    #for row in range(df.shape[0]):
        #common_enduse_df.loc[row] = A.dot(df.iloc[row, 3:])
    common_enduse_df = pd.DataFrame(data = np.dot(A, df[config.enduse_dict.keys()].to_numpy().transpose()).transpose() , columns = np.array(components_df['component']))

    load_temp = pd.DataFrame({'Date': df['Date'], 'power':df.iloc[:, 4:-2].sum(axis = 1), 'temp': df['drybulb']})

    common_enduse_df.insert(0, "Month", df["Mth"])
    common_enduse_df.insert(1, "Day", df["Dy"])
    common_enduse_df.insert(2, "Hour", df["Hr"])
    common_enduse_df.insert(0, 'Date', df["Date"])
    common_enduse_df["temp"] = df["drybulb"]
    return [common_enduse_df, df, load_temp, area_dict]

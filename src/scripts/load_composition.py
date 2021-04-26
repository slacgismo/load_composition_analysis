import pandas as pd
import numpy as np
import os
import datetime
from calendar import monthrange
import matplotlib.pyplot as plt
import sensitivity_new as sn
import setup_config
import user_config
import pickle
<<<<<<< HEAD


=======
>>>>>>> dc834c640f4f9cef874a90c3b1b73e3245535241
class config:
    eu_dict_ceus = dict(zip(
["heat_pump", "other_electric_heat", "cooling", "water_heating", "cooking"],
["Vent", "Heat", "Cool", "HotWater", "Cook"],
))
<<<<<<< HEAD
=======

>>>>>>> dc834c640f4f9cef874a90c3b1b73e3245535241
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
    rbsa_locations = pd.merge(pd.read_csv(setup_config.rbsa_locations), region_df, 'left', 'state')

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
    for csv in os.listdir(setup_config.rbsa_sites_folder) :
        if csv.endswith(".csv"):
            siteid_df_dict[csv.split('.')[0]] = pd.read_csv(setup_config.rbsa_sites_folder + csv, converters={"time":get_datetime})
    return siteid_df_dict

def find_csvfile(name):
    return str(sys.modules[__name__].__file__).replace(f"/loads.py",f"/{name}.csv")


electrification_index = ["location"]
electrification_data = ["heat_pump","other_electric_heat","cooling","water_heating","cooking"]
electrification_attributes = ["city","region","building_type"]
def load_electrification (
        select={},
        index="location",
        columns=["city","region","building_type","heat_pump",
            "other_electric_heat","cooling","water_heating","cooking"],
        convert=pd.DataFrame,
        version='latest'
        ):

    data = pd.read_csv(setup_config.electrification_data)
    for key,value in select.items():
        data = data[data[key]==value]
    return convert(data.set_index(index)[columns])

locations = pd.read_csv(setup_config.rbsa_locations)
locations['postcode'] = np.array(locations['postcode'])//100
siteid_zip = {}
for i in range(locations.shape[0]):
    siteid_zip[str(locations.iloc[i][0])] = locations.iloc[i][3]

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


def sensitivity_models(buildings, data, weekday, build_class):
    #if not os.path.isdir(btype):
     #   os.mkdir(btype)
    building_dict = data
    build_sens = {}
    build_enduses = {}
    if build_class == 'commercial':
        for btype in buildings:
            #temp = building_dict[btype].groupby('hour').mean()[['drybulb']]
            total_enduses = building_dict[btype].drop(columns = ['Mth', 'Dy', 'Hr'])
            #total_enduses = pd.merge(building_dict[btype].fillna(0).groupby('hour').mean().drop(columns = ['drybulb', 'Mth', 'Dy', 'Hr']), temp, left_index = True, right_index = True)
            #dates = np.array([datetime.datetime(t.year, t.month, t.day, t.hour) for t in total_enduses.index.values])
            total_enduses['weekday'] = [t.weekday() for t in pd.DatetimeIndex(total_enduses.index.values)]
            if weekday == 'weekday':
                total_enduses = total_enduses[total_enduses['weekday'] <=5].drop(columns = ['weekday'])
            elif weekday == 'weekend':
                total_enduses = total_enduses[total_enduses['weekday'] >5].drop(columns = ['weekday'])
            else:
                total_enduses = None
            ceus_enduses_df = {}
            sensitivities = {}
            for col in total_enduses.columns[:-1]:
                ceus_enduses_df[col] = pd.DataFrame({'power': total_enduses[col], 'temperature': total_enduses['drybulb']}, index = total_enduses.index.values)
                sensitivities[col] = sn.get_model_1(ceus_enduses_df[col], 0, 1, 2, col, dataset = 'ceus', saveplots = False)

            build_sens[btype] = sensitivities
            build_enduses[btype] = ceus_enduses_df
            print(btype)
    elif build_class == 'residential':
        total_enduses = data

        ceus_enduses_df = {}
        sensitivities = {}
        for col in total_enduses.columns[:-1]:
            ceus_enduses_df[col] = pd.DataFrame({'power': total_enduses[col], 'temperature': total_enduses['temp']}, index = total_enduses.index.values)
            sensitivities[col] = sn.get_model_1(ceus_enduses_df[col], 0, 1, 2, col, dataset = 'rbsa', saveplots = False)
        build_sens['RES'] = sensitivities
        build_enduses['RES'] = None
    return [build_sens, build_enduses]



if __name__ == "__main__":
    start = datetime.datetime.now()
    normed_load = {}
    for csv in sorted(os.listdir()):
        if csv.endswith('.csv'):
            filename = csv.split('.')[0]
            if filename.split('_')[1:] == ['enduse', 'data']:
                print(filename)
                normed_load[filename.split('_')[0]] = pd.read_csv(csv, converters = {'hour': get_datetime_ceus}).set_index('hour')
    ceus_sens = sensitivity_models(normed_load.keys(), normed_load, 'weekday', 'commercial')
    with open('ceus_sens.pickle', 'wb') as file:
        pickle.dump(ceus_sens, file)

    dt = lambda ts: datetime.datetime.strptime(ts,"%Y-%m-%d %H:%M:%S")
    rbsa_enduses = pd.read_csv('rbsa_enduses.csv')
    rbsa_enduses['index'] = [dt(t) for t in rbsa_enduses.rename(columns = {'Unnamed: 0': 'Date'}).set_index('Date').index.values]
    rbsa_enduses = rbsa_enduses.set_index('index').drop(columns = ['Unnamed: 0'])
    rbsa_sens = sensitivity_models(buildings = None, data = rbsa_enduses, weekday = 'weekday', build_class = 'residential')
    with open('rbsa_sens.pickle', 'wb') as file:
        pickle.dump(rbsa_sens, file)
    print((datetime.datetime.now() - start).total_seconds())
<<<<<<< HEAD
=======
    
>>>>>>> dc834c640f4f9cef874a90c3b1b73e3245535241

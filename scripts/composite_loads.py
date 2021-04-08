import pandas as pd
import numpy as np
import os
import datetime
from calendar import monthrange
import matplotlib.pyplot as plt
import sensitivity_new as sn
import git_setup_config as setup_config
#import user_config
import pickle
import requests
from csv import reader
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


def get_datetime(ts):
    return datetime.datetime.strptime(ts,"%d%b%y:%H:%M:%S")
def get_datetime_rbsa(ts):
    return datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
def noaa_datetime(ts):
    return datetime.datetime.strptime(ts,"%Y-%m-%d %H:%M:%S%z")

def get_datetime_ceus(ts):
    return datetime.datetime.strptime(ts,"%Y-%m-%d %H:%M:%S")
def config_cleaner(x):
    x2 = []
    for i in x:
        if i!=0:
            x2.append(i)
    return x2

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

def weather_season(location, day, aws, showplots = False):

    if day == "weekday":
        weekday = 1
    elif day == "weekend":
        weekday = 0
    else:
        weekday = None
    summer_months = [6,7,8,9]
    winter_months = [11,12,1,2]
    if aws == True:
        #print('aws')
        url = setup_config.aws_link %(location)
        r = requests.get(url, allow_redirects=True)
        open(f'{location}.csv', 'wb').write(r.content)
        loc = pd.read_csv(f'{location}.csv', converters = {"localtime": noaa_datetime})

    else:
        try:
            loc = pd.read_csv(setup_config.noaa_folder %(location), converters = {"localtime": noaa_datetime})
        except:
            os.system('python aws_pull.py')
            loc = pd.read_csv(setup_config.noaa_folder %(location), converters = {"localtime": noaa_datetime})
    time = [datetime.datetime(t.year, t.month, t.day, t.hour, 0, 0) for t in loc["localtime"]]
    loc["localtime"] = time
    loc["hr"] = [t.hour for t in loc["localtime"]]
    if weekday:
        loc["weekday"] = np.where(np.array([t.weekday() for t in loc["localtime"]]) < 5, 1, 0)
        loc = loc[loc["weekday"] == weekday]
        loc = loc.drop(columns = ["weekday"])

    loc["month"] = [t.month for t in loc["localtime"]]
    loc["date"] = [datetime.datetime(t.year, t.month, t.day, 0, 0, 0) for t in loc["localtime"]]
    loc_temp = loc[["heatindex", "hr"]]
    #loc_test = loc_temp[loc_temp["hr"] == 0]

    temps = {}
    #for i in [low, high]:
    loc_sum = loc[loc['month'].isin(summer_months)]
    loc_daily_max = loc_sum.groupby('date').max()
    thigh = np.percentile(loc_daily_max["heatindex"], 90)
    tot = sum(loc_daily_max["heatindex"] == round(thigh,1))
    #loc_daily_max = loc_daily_max[loc_daily_max["heatindex"] == round(thigh,1)]
    loc_daily_max = loc_daily_max[loc_daily_max["heatindex"].between(thigh - 0.5, thigh + 0.5)]
    #high_day = loc_daily_max.index.values[tot//2]
    #high_day = np.array(loc_daily_max.mean(axis = 0))
    #loc_day = loc[loc["date"] == high_day].groupby('localtime').mean()[["heatindex", "hr"]]
    loc_day = pd.merge(loc, pd.DataFrame({'date':loc_daily_max.index.values}), on = 'date', how = 'inner').groupby('hr').mean()
    loc_day['hr'] = loc_day.index.values
    loc_day = loc_day[['heatindex', 'hr']]
    high_day_temp = []
    count = 0
    for h in range(24):
        x = h-count
        if x >= loc_day.shape[0]:
            high_day_temp.append(loc_day["heatindex"][-1])
        elif h == 0:
            high_day_temp.append(loc_day["heatindex"][h])
        elif h == loc_day["hr"][x]:
            high_day_temp.append(loc_day["heatindex"][x])
        else:
            high_day_temp.append(high_day_temp[-1])
            count+=1
    loc_wint = loc[loc['month'].isin(winter_months)]
    loc_daily_min = loc_wint.groupby('date').min()
    tlow = np.percentile(loc_daily_min["heatindex"], 10)
    tot = sum(loc_daily_min["heatindex"] == round(tlow,1))
    loc_daily_min = loc_daily_min[loc_daily_min["heatindex"].between(tlow - 0.5, tlow + 0.5)]
    #low_day = loc_daily_min.index.values[tot//2]
    #low_day = np.array(loc_daily_min.mean(axis = 0))
    #loc_day = loc[loc["date"] == low_day].groupby('localtime').mean()[["heatindex", "hr"]]
    loc_day = pd.merge(loc, pd.DataFrame({'date':loc_daily_min.index.values}), on = 'date', how = 'inner').groupby('hr').mean()
    loc_day['hr'] = loc_day.index.values
    loc_day = loc_day[['heatindex', 'hr']]
    low_day_temp = []
    count = 0
    for h in range(24):
        x = h-count
        if x >= loc_day.shape[0]:
            low_day_temp.append(loc_day["heatindex"][-1])
        elif h == 0:
            low_day_temp.append(loc_day["heatindex"][h])
        elif h == loc_day["hr"][x]:
            low_day_temp.append(loc_day["heatindex"][x])
        else:
            low_day_temp.append(low_day_temp[-1])
            count+=1

    spring_temp = np.array(loc[loc['month'].between(4,6)].groupby('hr').mean()['heatindex'])

    return [low_day_temp, spring_temp, high_day_temp]

def loadshape(location, sensitivities, day, weather, btype, showplots = False):
    low_day_temp = weather[0]
    spring_temp = weather[1]
    high_day_temp = weather[2]
    load_dict = {}
    for col in sensitivities.keys():
        p=[]
        q=[]
        r=[]
        model = sensitivities[col]

        for h in range(24):

            try:
                p.append(sn.get_load(model,h,np.array(low_day_temp)[h],normalize=False, convert = list)[0])
            except:
                p.append(sn.get_load(model,h,np.array(low_day_temp)[h],normalize=False, convert = None))
            try:
                q.append(sn.get_load(model,h,spring_temp[h],normalize=False, convert = list)[0])
            except:
                q.append(sn.get_load(model,h,spring_temp[h],normalize=False, convert = None))
            try:
                r.append(sn.get_load(model,h,np.array(high_day_temp)[h],normalize=False, convert = list)[0])
            except:
                r.append(sn.get_load(model,h,np.array(high_day_temp)[h],normalize=False, convert = None))
        #for load in [p,q,r]:
            #load = np.where(np.array(load) < 0, 0, np.array(load))
        p = np.where(np.array(p) < 0, 0, np.array(p))
        q = np.where(np.array(q) < 0, 0, np.array(q))
        r = np.where(np.array(r) < 0, 0, np.array(r))
        #p = np.array(get_load(model,h,[np.array(low_day_temp)],normalize=False)).flatten()
        plow = p - np.ones(len(p))*3*np.std(p)
        phigh = p + np.ones(len(p))*3*np.std(p)
        #q = np.array(get_load_orig(model,h,[np.array(new_tcool)],normalize=False)).flatten()
        qlow = q - np.ones(len(q))*3*np.std(q)
        qhigh = q + np.ones(len(q))*3*np.std(q)
        #r = np.array(get_load_orig(model,h,[np.array(high_day_temp)],normalize=False)).flatten()
        rlow = r - np.ones(len(r))*3*np.std(r)
        rhigh = r + np.ones(len(r))*3*np.std(r)


        plt.plot(p, color = 'r')
        #plt.plot(plow,'--', color = 'r')
        plt.plot(phigh,'--', color = 'r')
        plt.plot(r, color = 'b')
        #plt.plot(rlow,'--', color = 'b')
        plt.plot(rhigh,'--', color = 'b')
        plt.plot(q, color = 'y')
        #plt.plot(qlow,'--', color = 'y')
        plt.plot(qhigh,'--', color = 'y')
        plt.xlabel("Hour of day")
        plt.ylabel("Load (kW/sqft)")
        plt.title("Loadshape for %s %s %s %s" %(location, btype, col, day))
        plt.grid()
        #plt.close()
        #plt.savefig("noaa_loadshape/%s/%s_loadshape.png" %(location, day))
        #plt.legend(t.keys())
        if showplots:
            #plt.show()
            plt.savefig(f'{location}/Loadshape_{location}_{btype}_{col}_{day}.png')
            plt.close()
        load_dict[col] = np.array([p,q,r])

    return load_dict



def comp_enduses(weather, ceus_sens, rbsa_sens, location, feeder, electrification, debug = False, showplots = False):
    regional_electrification = {}
    for i in set(electrification["region"]):
        x = {}
        for j in ["commercial", "residential"]:
            x[j] = electrification[(electrification["region"] == i) & (electrification["building_type"] == j)].iloc[0][3:]
        regional_electrification[i] = x
    build_map = {'college': 'COLL',
     'grocery' : 'GROC',
     'health' : 'HLTH',
     'home' : 'RES',
     'large_office': 'LOFF',
     'lodging': 'LODG',
     'miscellaneous': 'MISC',
     'refrigerated_warehouse': 'RWHS',
     'restaurant': 'REST',
     'retail' : 'RETL',
     'school' : 'SCHL',
     'small_office': 'SOFF',
     'warehouse': 'WRHS'}
    if location == 'ORH':
        location = 'ORD'
    feeder_comp = pd.read_csv(setup_config.feeder_comp)
    sens = ceus_sens
    #sens[0]['RES'] = rbsa_sens[0]['RES']
    #winter_build = []
    #spring_build = []
    #summer_build = []
    com_load_dict = {}
    for btype in sens[0].keys():

        if not os.path.isdir(location):
            os.mkdir(location)
        #if not os.path.isdir('%s/%s' %(location, 'composite')):
        #    os.mkdir('%s/%s' %(location, 'composite'))
        #if not os.path.isdir('%s/%s' %(location,  feeder)):
        #    os.mkdir('%s/%s/%s' %(location, 'composite', feeder))


        tot_eu_ceus = {}
        tot_eu_rbsa = {}
        sensitivities = sens[0][btype]


        eu_new = []
        for i in sensitivities.keys():
            eu_new.append(config.res_comp_dict_ceus[i])

        components_df = pd.read_csv(setup_config.roa_matrix)
        res_comp = components_df[components_df['building_type'] == get_keys(config.btype_dict, btype)].dropna(axis = 1)
        res_comp_mat = res_comp[eu_new].to_numpy()
        #sensitivities = sensitivties[zone]
        winter = []
        spring = []
        summer = []
        if showplots:
            print(btype)
        loads = loadshape(location, sensitivities, 'weekday', weather, btype = btype, showplots = showplots)
        try:
            area, bcount = feeder_comp[(feeder_comp['feeder_type'] == feeder) & (feeder_comp['building_type'] == inverse_mapping(build_map)[btype])].iloc[0][3:]
        except:
            area = 0
            bcount = 0
        g = {}
        for eu in sensitivities.keys():
            load = loads[eu]
            loc = electrification[(electrification.index.values == location)]

            try:
                elec = loc[loc['building_type'] == 'commercial'][config.eu_dict_elec_ceus[eu]][0]
            except:
                elec = 1
            #if eu == 'Cool':
             #   elec = elec/10

            winter.append(np.where(load[0]>0, load[0], 0)*elec)
            spring.append(np.where(load[1]>0, load[1], 0)*elec)
            summer.append(np.where(load[2]>0, load[2], 0)*elec)


            g[eu] = {'winter': load[0], 'spring': load[1], 'summer': load[2]}
            if debug:
                print(elec)
        winter = np.dot(res_comp_mat, np.array(winter)*area*bcount)
        spring = np.dot(res_comp_mat, np.array(spring)*area*bcount)
        summer = np.dot(res_comp_mat, np.array(summer)*area*bcount)
        com_load_dict[btype] = g
        try:
            winter_build = winter_build + np.array(winter)
        except:
            winter_build = np.array(winter)
        try:
            spring_build = spring_build + np.array(spring)
        except:
            spring_build = np.array(spring)
        try:
            summer_build = summer_build + np.array(summer)
        except:
            summer_build = np.array(summer)
        if debug:
            print(area, bcount)


    #for col in range(len(sensitivities.keys())):
     #   tot_eu_ceus[list(sensitivities.keys())[col]] = {'winter': winter_build[col], 'spring': spring_build[col], 'summer': summer_build[col]}
    for season in [winter_build, spring_build, summer_build]:
        df = pd.DataFrame(season)
        df.fillna(method='ffill', axis=1, inplace=True)
        season = df.to_numpy()
    winter_build_load = winter_build
    spring_build_load = spring_build
    summer_build_load = summer_build

    sens = rbsa_sens


    hc_ind = list(sens[0]['RES'].keys()).index('hc')
    cooling_ind = list(sens[0]['RES'].keys()).index('cooling')
    indexes = [hc_ind, cooling_ind]
    for btype in sens[0].keys():
        sensitivities = sens[0][btype]
        eus = list(sensitivities.keys())
        eus.remove('hc')
        eu_new = []
        for i in eus:
            eu_new.append(inverse_mapping(config.res_comp_dict_rbsa)[i])
        #eu_new = sensitivities.keys()
        components_df = pd.read_csv(setup_config.roa_matrix)
        res_comp = components_df[components_df['building_type'] == get_keys(config.btype_dict, btype)].dropna(axis = 1)
        res_comp_mat = res_comp[eu_new].to_numpy()

        winter = []
        spring = []
        summer = []

        loads = loadshape(location, sensitivities, 'weekday', weather, btype = btype, showplots = showplots)
        try:
            area, bcount = feeder_comp[(feeder_comp['feeder_type'] == feeder) & (feeder_comp['building_type'] == inverse_mapping(build_map)[btype])].iloc[0][3:]
        except:
            area = 0
            bcount = 0
        for eu in sensitivities.keys():
            load = loads[eu]
            loc = electrification[(electrification.index.values == location)]

            try:
                elec = loc[loc['building_type'] == 'residential'][inverse_mapping(config.eu_dict_elec)[eu]][0]
            except:
                elec = 1
            #if eu == 'cooling':
             #   elec = elec*10
            if hc_ind < cooling_ind:
                if eu == 'hc':
                    add_load = [np.where(load[0]>0, load[0], 0)*elec,np.where(load[0]>0, load[1], 0)*elec,np.where(load[0]>0, load[2], 0)*elec]
                elif eu == 'cooling':
                    winter.append(np.where(load[0]>0, load[0], 0)*elec + add_load[0])
                    spring.append(np.where(load[1]>0, load[1], 0)*elec + add_load[1])
                    summer.append(np.where(load[2]>0, load[2], 0)*elec + add_load[2])
                else:
                    winter.append(np.where(load[0]>0, load[0], 0)*elec)
                    spring.append(np.where(load[1]>0, load[1], 0)*elec)
                    summer.append(np.where(load[2]>0, load[2], 0)*elec)
            else:
                if list(sensitivities.keys()).index(eu) == max(indexes):
                    winter[min(indexes)] = winter[min(indexes)] + np.where(load[0]>0, load[0], 0)*elec
                    spring[min(indexes)] = spring[min(indexes)] + np.where(load[1]>0, load[1], 0)*elec
                    summer[min(indexes)] = summer[min(indexes)] + np.where(load[2]>0, load[2], 0)*elec
                else:
                    winter.append(np.where(load[0]>0, load[0], 0)*elec)
                    spring.append(np.where(load[1]>0, load[1], 0)*elec)
                    summer.append(np.where(load[2]>0, load[2], 0)*elec)
            if debug:
                print(elec)


        winter_build += np.dot(res_comp_mat, np.array(winter)*area*bcount)
        spring_build += np.dot(res_comp_mat, np.array(spring)*area*bcount)
        summer_build += np.dot(res_comp_mat, np.array(summer)*area*bcount)

    #for col in range(len(eus)):
     #   tot_eu_rbsa[eus[col]] = {'winter': winter_build[col], 'spring': spring_build[col], 'summer': summer_build[col]}

    winter_build_load = winter_build#.transpose()
    spring_build_load =spring_build#.transpose()
    summer_build_load = summer_build#.transpose()


    season_dict = {'winter': winter_build_load, 'spring': spring_build_load, 'summer': summer_build_load}
    for season in ['winter', 'spring', 'summer']:
        if not os.path.isdir('%s/%s' %(location, season)):
            os.mkdir('%s/%s' %(location, season))
        if not os.path.isdir('%s/%s/%s' %(location, season, feeder)):
            os.mkdir('%s/%s/%s' %(location, season, feeder))
        arr = season_dict[season]/sum(season_dict[season])
        #print(arr)
        #for i in range(len(arr)):
         #   for j in range(len(arr[i])):
          #      arr[i][j] = round(j*100, 1)
        labels = list(res_comp['component'])
        #labels.reverse()
        df = pd.DataFrame(arr)
        print(df)
        #df.insert(0, 'Component', np.array(res_comp['component']))
        df.insert(0, 'Component', np.array(['MOTOR A', 'MOTOR B', 'MOTOR C', 'MOTOR D', 'POWER ELECTRONICS', 'CONSTANT IMPEDANCE', 'CONSTANT CURRENT']))
        #df = df.set_index('Component')
        df.to_csv('%s/%s/%s/%s_%s_%s.csv' %(location, season, feeder, location, season, feeder), index = False)
        df = df.set_index('Component').T
        df.insert(0, 'Hour', df.index.values)
        df.to_csv('%s/%s/%s/%s_%s_%s_transposed.csv' %(location, season, feeder, location, season, feeder), index = False)
        #plt.figure(figsize = (18,6))
        fig, ax = plt.subplots(1,2, figsize = (18,6))
        #plt.show()
        ax[0].stackplot(np.arange(24),season_dict[season]/sum(season_dict[season]), labels=labels)
        ax[0].legend(loc='upper left')
        ax[0].set_title('Normalized Hourly composite %s enduse load for %s' %(feeder, location))
        ax[0].set_xlabel('Hour of the day')
        ax[0].set_ylabel('Load Proportion (kW per sqft/total kW per sqft)')
        ax[0].set_xticks(np.arange(0,24,6))
        ax[1].stackplot(np.arange(24),season_dict[season], labels=labels)
        ax[1].legend(loc='upper left')
        ax[1].set_title('Hourly composite %s enduse load for %s' %(feeder, location))
        ax[1].set_xlabel('Hour of the day')
        ax[1].set_ylabel('Load (kW per sqft)')
        ax[1].set_xticks(np.arange(0,24,6))
        plt.savefig('%s/%s/%s/%s_%s_%s.png' %(location, season, feeder, location, season, feeder))
        plt.close()


    return [season_dict, com_load_dict]#, tot_eu_ceus, tot_eu_rbsa]

if __name__ == "__main__":
    config_dict = {}
    with open('../user_config.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            row_new = []
            for r in row:
                if r != "":
                    row_new.append(r)
                    config_dict[row_new[0]] = row_new[1:]
    #config_df = pd.read_csv('user_config.csv').fillna(0)
    cities = config_dict['City']
    seasons = config_dict['Season']
    ftype = config_dict['Feeder']
    debug = config_dict['Intermediate Results']
    if len(seasons) == 0:
        seasons = ['Summer', 'Winter', 'Spring']
    if len(ftype) == 0:
        ftype = ['residential', 'commercial', 'mixed', 'rural']
    open("file_loc.txt", "w").close()
    open("debug_loc.txt", "w").close()
    with open(f'../data/ceus_sens.pickle', 'rb') as file:
        ceus_sens = pickle.load(file)
    with open(f'../data/rbsa_sens.pickle', 'rb') as file:
        rbsa_sens = pickle.load(file)
    electrification = load_electrification()
    for city in cities:
        #city = city.lower()
        if not os.path.isdir(city):
            os.mkdir(city)
        f = open("debug_loc.txt", "a")
        f.write(f'{city}' + "\n")
        if 'weather' in debug:
            weather = weather_season(location = city, day = 'weekday', aws = True)
            fig, ax = plt.subplots(figsize = (10,8))
            ax.plot(weather[0], color = 'red', label = 'winter')
            ax.plot(weather[1], color = 'yellow', label = 'spring')
            ax.plot(weather[2], color = 'blue', label = 'summer')
            ax.set_xlabel('Hour of the Day')
            ax.set_ylabel('Heat Index (F)')
            ax.set_title(f'{city} Weather Profile')
            ax.legend()
            plt.savefig(f'{city}/{city}_weather_profile.png')
            plt.close()
        else:
            weather = weather_season(location = city, day = 'weekday', aws = True)
        for feeder in ftype:
            feeder = feeder.lower()
            if 'loadshape' in debug:
                comp_enduses(weather = weather, ceus_sens = ceus_sens, rbsa_sens = rbsa_sens, location = city, feeder = feeder, electrification = electrification, showplots = True)
            else:
                comp_enduses(weather = weather, ceus_sens = ceus_sens, rbsa_sens = rbsa_sens, location = city, feeder = feeder, electrification = electrification, showplots = False)
            for season in seasons:
                #season = season.lower()
                f = open("file_loc.txt", "a")
                f.write(f'{city}/{season.lower()}/{feeder}' + "\n")

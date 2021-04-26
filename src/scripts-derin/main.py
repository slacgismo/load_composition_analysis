import os
import pickle
import pathlib
import numpy as np
import pandas as pd
from helpers import *
import sensitivity_new as sn

if __name__ == "__main__":
    # set absolute path
    path = os.path.abspath(os.getcwd())

    config_settings = pd.read_csv(os.path.join(path, pathlib.Path('config.csv')), header = None).fillna('')
    config_settings = config_settings.rename(columns = {0: "Category", 1: "Values"})
    cities = np.array(config_settings[config_settings["Category"] == 'City' ]['Values'])[0].split()
    seasons = np.array(config_settings[config_settings["Category"] == 'Season' ]['Values'])[0].split()
    ftype = np.array(config_settings[config_settings["Category"] == 'Feeder' ]['Values'])[0].split()
    debug = np.array(config_settings[config_settings["Category"] == 'Intermediate Results' ]['Values'])[0].split()

    open(path_adder(path,"file_loc.txt"), "w").close()
    open(path_adder(path, "debug_loc.txt"), "w").close()
    with open(path_adder(path, 'data/ceus_sens.pickle'), 'rb') as file:
        ceus_sens = pickle.load(file)
    with open(path_adder(path, 'data/rbsa_sens.pickle'), 'rb') as file:
        rbsa_sens = pickle.load(file)
    electrification = load_electrification()
    for city in cities:
        print(city)
        if not os.path.isdir(city):
            os.mkdir(city)
        f = open(path_adder(path, "debug_loc.txt"), "a")
        f.write(f'{city}' + "\n")
        # if 'weather' in debug:
        #     weather = weather_season(location = city, day = 'weekday', aws = True)
        #     fig, ax = plt.subplots(figsize = (10,8))
        #     ax.plot(weather[0], color = 'red', label = 'winter')
        #     ax.plot(weather[1], color = 'yellow', label = 'spring')
        #     ax.plot(weather[2], color = 'blue', label = 'summer')
        #     ax.set_xlabel('Hour of the Day')
        #     ax.set_ylabel('Heat Index (F)')
        #     ax.set_title(f'{city} Weather Profile')
        #     ax.legend()
        #     plt.savefig(path_adder(path, f'{city}/{city}_weather_profile.png'))
        #     plt.close()
        # else:
        #     weather = weather_season(location = city, day = 'weekday', aws = True)
        # if len(ftype) == 0:
        #     print('You have not selected a feeder type. Please input one or more of the following options: Residential, Commercial, Mixed, Rural')
        # if len(seasons) == 0:
        #     print('You have not selected a season. Please input one or more of the following options: Summer, Spring, Winter')
        # for feeder in ftype:
        #     feeder = feeder.lower()
        #     if 'loadshape' in debug:
        #         comp_enduses(weather = weather, ceus_sens = ceus_sens, rbsa_sens = rbsa_sens, location = city, feeder = feeder, path = path, electrification = electrification, showplots = True)
        #     else:
        #         comp_enduses(weather = weather, ceus_sens = ceus_sens, rbsa_sens = rbsa_sens, location = city, feeder = feeder, path = path, electrification = electrification, showplots = False)
        #     for season in seasons:
        #         #season = season.lower()
        #         f = open(path_adder(path, "file_loc.txt"), "a")
        #         f.write(f'{city}/{season.lower()}/{feeder}' + "\n")

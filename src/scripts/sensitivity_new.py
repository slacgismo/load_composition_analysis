"""Weather sensitivity analysis
"""
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import pwlf

class config:
    """Load model analysis configuration

Load modeling:

    Tdiff   Difference between the heating and cooling balance temperatures
            (default 10 degF)

    Tbase   Base temperature for the heating and cooling balance temperature
            (default is 60 degF)

    Days    Weekdays to include in developing the load model
            (default is Monday through Friday, i.e., [0,1,2,3,4])

Row filtering:

    Tmin    The minimum temperature to accept (inclusive) when loading data
            (default is -50 degF)

    Tmax    The maximum temperature to accept (inclusive) when loading data
            (default is 130 degF).

    Pmin    The minimum power to accept (exclusive) when loading data
            (default 0)

    Pmax    The maximum power to accept (exclusive) when loading data
            (default None)

Processing:

    SavePlots       Enables plots of intermediate results to be generated
                    (default False)

    DatetimeFormat  The date/time format to use when reading timestamps
                    (default mm/dd/yy HH:MM)

    NullValue       The value used to indicated a bad/missing value
                    (default NaN)

    SkipRows        The number of rows to skip when loading data
                    (default 1)

    MaxIterations   The maximum number of iterations allowing when getting
                    the base temperature (default 50)

    Model           The type of model to use, i.e., 0=fixed-width, 1=general
                    (default 0)

    """
    Tdiff = 10.0
    Tbase = 60.0
    Days = [0,1,2,3,4]
    Tmin = -50.0
    Tmax = 130.0
    Pmin = 0.0
    Pmax = None
    SavePlots = True
    DatetimeFormat = '%m/%d/%y %H:%M'
    NullValue = float('nan')
    SkipRows = 1
    MaxIterations = 50
    Model = 1

weather_enduses = {'sensitive': ['Cool', 'Heat'], 'insensitive': ['Process','Vent', 'AirComp', 'Refrig', 'Motors', 'OffEquip', 'Misc', 'ExtLight', 'Cook', 'HotWater', 'IntLight']}
weather_enduses_rbsa = {'sensitive' : ['cooling', 'heating'], 'insensitive': ['computer', 'dryer', 'entertainment', 'freezer', 'lighting', 'other', 'oven', 'plug', 'refrig', 'washer', 'waterheat']}
btype_dict = {'office': ['LOFF'], 'lodging': ['LODG'], 'commercial': ['AWHS', 'COLL', 'GROC', 'HLTH', 'MISC', 'REFW', 'REST', 'RETL', 'SCHL', 'WRHS', 'AOFF', 'SOFF'], 'residential' : ['RES']}
def get_keys(dictionary, val):
    for key, value in dictionary.items():
         if val in value:
            return key

    return "key doesn't exist"

def dot_check(x1, y1, i_0, i_1):
    return np.array([x1[i_1]-x1[i_0], (y1[i_1]-y1[i_0])*10000]).dot(np.array([1,0]))/(np.linalg.norm(np.array([x1[i_1]-x1[i_0], (y1[i_1]-y1[i_0])*10000])))

def read_datetime(x,format=config.DatetimeFormat):
    """
    Default datetime reader

	Use config.DatetimeFormat to change the datetime reader format, e.g.,

		load_model.config.DatetimeFormat = '%Y/%m/%m %H:%M:%S'
    """
    return dt.datetime.strptime(x,format)

def read_float(x,null=config.NullValue):
    """
    Default value reader

	Use config.NullValue to change the float reader format, e.g.,

		load_model.config.NullValue = float('nan')
    """
    try:
        return float(x)
    except:
        return null

def load_data(ifile,
        datetime_col = 0,
        power_col = 1,
        temperature_col = 2,
        humidity_col = None,
        names = {0:'datetime',1:'power',2:'temperature'},
        skiprows = config.SkipRows,
        filter = True,
        dropna = True):
    """
    Load data from CSV file

    Parameters:

        ifile (str)                  input file name

        datetime_col (datetime)      datetime column number (default 0)

        power_col (int)              power column number (default 1)

        temperature_col (int)        temperature column number (default 2)

        humidity (int)               humidity column number (default None)

        skiprows (int)               rows skipped when reading (default 1)

        filter (bool or callable)    filter enable/function (default True)

        dropna (bool, str, or list)  dropna flag, 'any','all', or list of
                                     column names in which na is found

    Returns:

        DataFrame - contains loaded data

    The data loader imports the specified CSV file, using the optional column
    specifications and filter, and returns the result as a DataFrame.
    """
    data = pd.read_csv(ifile,
            low_memory=False,
            header=None,
            skiprows=skiprows,
            index_col=0,
            converters={datetime_col:read_datetime,power_col:read_float,temperature_col:read_float},
            usecols=[datetime_col,power_col,temperature_col],
            names=[names[datetime_col],names[power_col],names[temperature_col]])
    if callable(filter):
        filter(data,inplace=True)
    elif filter:
        if not config.Tmax == None: data.drop(data[data[names[temperature_col]]>config.Tmax].index,inplace=True)
        if not config.Tmin == None: data.drop(data[data[names[temperature_col]]<config.Tmin].index,inplace=True)
        if not config.Pmin == None: data.drop(data[data[names[power_col]]<=config.Pmin].index,inplace=True)
        if not config.Pmax == None: data.drop(data[data[names[power_col]]>=config.Pmax].index,inplace=True)
    if dropna is str:
        data.dropna(how=dropna,inplace=True)
    elif dropna is list:
        data.dropna(subset=dropna,inplace=True)
    elif dropna == True:
        data.dropna(inplace=True)
    return data

def get_days(data,days=config.Days):
    """
    Get the data for the desired weekdays

    Parameters:

        data (DataFrame)    data set

        days (list)         weekdays to include in data

    Returns:

        DataFrame           data that includes specified weekdays
    """
    return data[data.index.dayofweek.isin(days)]

def get_hours(data,hours):

    """
    Get the data for the desired hours

    Parameters:

        data (DataFrame)    data set

        hours (list)        hours to include in data

    Returns:

        DataFrame            data that includes specified hours
    """
    try:
        return data[data.index.hour.isin(hours)]
    except:
        h = []
        for i in data.index.values:
            h.append(pd.to_datetime(i).hour)
        data['hour'] = h
        return data[data['hour'].isin(hours)].drop(columns = ['hour'])

def get_baseload(data,
        power_name,
        temperature_name,
        Tbase = 'auto',
        Tdiff = config.Tdiff,
        MaxSlope = 0.1,
        Epsilon = 0.1,
        ):
    """
    Get the base load model

    Parameters:

        data (DataFrame)        data to use in computing the baseload

        Tbase (float or 'auto') base temperature to use, 'auto' will find the
                                base temperature that minimum the abs(slope)
                                (default 'auto')

        Tdiff (float)           base load temperature band
                                (default 10 degF)

        MaxSlope (float)        maximum slope allowed when finding base
                                (default 0.1)

        Epsilon (float)         slope discount factor to use when updating Tbase
                                (default 0.1)

    Returns:

        load (float)        Base load value at Tbase

        slope (float)        Slope of the base at Tbase

        Tbase (float)        Base temperature that minimizes abs(slope) in degF

        base (DataFrame)    The base load data used to find Tbase

    The base load is obtained by computing the mean load of the data set where
    the temperature is within Tdiff/2 of Tbase.  If Tbase is 'auto' a linear
    regression is performed iteratively until the value of Tbase that minimizes
    the slope is found.
    """
    if Tbase == 'auto':
        slope=np.Infinity
        Tbase = config.Tbase
        n = 1
        while abs(slope) > MaxSlope and n < config.MaxIterations:
            base = data[(data[temperature_name]-Tbase).abs()<=Tdiff/2]
            T = np.array(base[temperature_name])
            P = np.array(base[power_name])
            slope, intercept, rvalue, pvalue, stderr = st.linregress(T,P)
            Tbase -= slope * (Epsilon/n)
            load = intercept + slope*Tbase
            n += 1
    else:
        base = data[(data[temperature_name]-Tbase).abs()<=Tdiff/2]
        T = np.array(base[temperature_name])
        P = np.array(base[power_name])
        slope, intercept, rvalue, pvalue, stderr = st.linregress(T,P)
        load = intercept + slope*Tbase
    return load, slope, Tbase, base

def get_sensitivity(heating,cooling,power_name,temperature_name):
    """Get heating and cooling load sensitivity to temperature

    Parameters:

        heating (DataFrame)        data set for heating

        cooling (DataFrame)        data set for cooling

        power_name (str)        power column name

        temperature_name (str)     temperature column name

    Returns:

        heat_slope (float)    heating temperature sensitivity in MW/degF

        cool_slope (float)    cooling temperature sensitivity in MW/degF

    Performs a linear regression on the data set to determine the slope
    of the power w.r.t temperature.
    """

    if not heating.empty:
        T = np.array(heating[temperature_name])
        P = np.array(heating[power_name])
        heat_slope, h0, hr, hp, hs = st.linregress(T,P)
    else:
        heat_slope = None

    if not cooling.empty:
        T = np.array(cooling[temperature_name])
        P = np.array(cooling[power_name])
        cool_slope, c0, cr, cp, cs = st.linregress(T,P)
    else:
        cool_slope = None

    return heat_slope, cool_slope

def get_load(model,hour,temperature,convert=list,normalize=False):
    """Get loads for given hours and temperature

    Parameters:
        model (DataFrame) - Load model from get_model()
        hour (list-like) - Hours to consider
        temperature (list-like) - Temperatures to consider
        convert (callable) - return result conversion function
        normalize (boolean) - enable result normalization

    Returns: float, list-like, or output of 'convert'
    """
    if config.Model == 0:
        return get_load_0(model,hour,temperature,convert=list,normalize=False)
    elif config.Model == 1:
        return get_load_1(model,hour,temperature,convert=list,normalize=False)
    else:
        raise Exception(f"config.Model = {config.Model} is not valid")

def get_load_0(model,hour,temperature,convert,normalize):
    def normal(x,normalize):
        if normalize:
            x = np.array(x)
            return x/x.max()
        else:
            return x
    if type(hour) is int:
        if type(temperature) is float:
            Sbase = model["Sbase"][hour]
            Pbase = model["Pbase"][hour]
            Theat = model["Theat"][hour]
            Tcool = model["Tcool"][hour]
            Tbase = 0.5*Theat + 0.5*Tcool
            if temperature < Theat:
                Sheat = model["Sheat"][hour]
                Theat = model["Theat"][hour]
                Ptemp = Sbase*(Theat-Tbase) + Sheat*(temperature-Theat)
            elif temperature > Tcool:
                Scool = model["Scool"][hour]
                Tcool = model["Tcool"][hour]
                Ptemp = Sbase*(Tcool-Tbase) + Scool*(temperature-Tcool)
            else:
                Ptemp = Sbase*(temperature-Tbase)
            return Pbase + Ptemp
        else:
            result = []
            for t in temperature:
                result.append(get_load(model,hour,float(t)))
    elif type(temperature) is float:
        result = []
        for h in hour:
            result.append(get_load(model,int(h),temperature))
    else:
        result = []
        for h in hour:
            data = []
            for t in temperature:
                data.append(get_load(model,int(h),float(t)))
            result.append(data)
    return convert(normal(result,normalize))

def get_load_1(model,hour,temperature,convert,normalize):
    return model[hour].predict(temperature)

def get_model(data, datetime_col, power_col, temperature_col, enduse, dataset,
        skiprows=config.SkipRows,
        ofile=None,
        saveplots=config.SavePlots):
    """Get load model

    Parameters:

        data (DataFrame)          input file name (required)

        datetime_col (int)        datetime column number (required)

        power_col (int)           power column number (required)

        temperature_col (int)     temperature column number (required)

        skiprows (int)            rows to skip before reading data (default 1)

        ofile (str)               output file name (default None)

        saveplots (bool)          plot saving flag (default False)

    Returns:

        DataFrame - load model

    The load model contains the following data for each hour of day

        Pbase    base load in the balance temperature band Tdiff (MW)

        Pheat    peak heating load at Tmin (MW)

        Pcool     peak cooling load at Tmax (MW)

        Tmin    minimum observed temperature (degF)

        Theat     heating balance temperature (degF)

        Tcool     cooling balance temperature (degF)

        Tmax     maximum observed temperature (degF)

        Sbase     base load temperature sensitivity (MW/degF)

        Sheat     heating load temperature sensitivity (MW/degF)

        Scool     cooling load temperature sensitivity (MW/degF)

    """
    if config.Model == 0:
        return get_model_0(data,datetime_col,power_col,temperature_col, enduse,
            skiprows,ofile,saveplots)
    elif config.Model == 1:
        return get_model_1(data,datetime_col,power_col,temperature_col, enduse,
            skiprows,ofile,saveplots)
    else:
        raise Exception(f"config.Model = {config.Model} is not valid")

def get_model_0(data, datetime_col, power_col, temperature_col, enduse = None, dataset = None,
        skiprows=config.SkipRows,
        ofile=None,
        saveplots=config.SavePlots):
    """See get_model()"""
    column_list = list(data.columns)
    column_list.insert(0,'datetime')
    power_name = column_list[power_col]
    temperature_name = column_list[temperature_col]
    days = get_days(data=data,days=config.Days)
    model = {"Hour":[],
        "Pbase":[], "Pheat":[], "Pcool":[],
        "Tmin":[], "Theat":[], "Tcool":[], "Tmax":[],
        "Sbase":[], "Sheat":[], "Scool":[]}

    for h in range(0,24):

        hour = get_hours(data=days,hours=[h])

        load, base, Tbal, neither = get_baseload(hour,power_name=power_name,temperature_name=temperature_name)

        heating = hour[hour[temperature_name]<Tbal-config.Tdiff/2]
        cooling = hour[hour[temperature_name]>Tbal+config.Tdiff/2]

        heat, cool = get_sensitivity(heating=heating,cooling=cooling,power_name=power_name,temperature_name=temperature_name)

        Tlo = hour[temperature_name].min()
        Thi = hour[temperature_name].max()

        Theat = Tbal - config.Tdiff/2
        Tcool = Tbal + config.Tdiff/2
        Pheat = load + (Tlo-Theat)*heat
        Pcool = load + (Thi-Tcool)*cool

        model["Hour"].append(h)
        model["Pbase"].append(load)
        model["Pheat"].append(Pheat)
        model["Pcool"].append(Pcool)
        model["Tmin"].append(Tlo)
        model["Theat"].append(Tbal-config.Tdiff/2)
        model["Tcool"].append(Tbal+config.Tdiff/2)
        model["Tmax"].append(Thi)
        model["Sbase"].append(base)
        model["Sheat"].append(heat)
        model["Scool"].append(cool)

        if saveplots:

            plt.figure()
            plt.plot(heating[temperature_name],heating[power_name],'.r')
            plt.plot(cooling[temperature_name],cooling[power_name],'.b')
            plt.plot(neither[temperature_name],neither[power_name],'.y')
            plt.plot([Tlo,Theat,Tcool,Thi],[Pheat,load,load,Pcool],'k')
            plt.grid()
            plt.legend(['Heating','Cooling','Baseload','Profile'],loc=9)
            plt.xlabel('Temperature (degF)')
            plt.ylabel('Load (MW)')
            plt.title(f'Load profile for hour {h}')
            plt.savefig('%s-profile-%02d.png'%(power_name,h))
            plt.close()

    model = pd.DataFrame(model).set_index("Hour")

    if ofile:
        model.to_csv(ofile)

    if saveplots:

        Hour = model.index
        Tbal = (model["Theat"]+model["Tcool"])/2
        Pbase = model["Pbase"]
        Pheat = model["Pheat"]
        Pcool = model["Pcool"]
        Sheat = model["Sheat"]
        Sbase = model["Sbase"]
        Scool = model["Scool"]

        plt.figure()
        plt.plot(Pbase,Tbal,'.')
        plt.grid()
        plt.xlabel('Base load (MW)')
        plt.ylabel('Balance temperature (degF)')
        plt.title('Balance temperature vs Base load')
        plt.savefig(f'{power_name}-balance-load.png')
        plt.close()

        plt.figure()
        plt.plot(Hour,Tbal)
        plt.grid()
        plt.xlabel("Hour of day")
        plt.ylabel("Balance temperature (degF)")
        plt.title(f'Balance temperature (+/- {config.Tdiff/2} degF)')
        plt.savefig(f"{power_name}-loadshape.png")
        plt.close()

        plt.figure()
        plt.plot(Hour,Pbase,'y')
        plt.plot(Hour,Pheat,'r')
        plt.plot(Hour,Pcool,'b')
        plt.grid()
        plt.xlabel("Hour of day")
        plt.ylabel('Load (MW)')
        plt.title('Load shapes')
        plt.legend(["Base load","Peak heating","Peak cooling"])
        plt.savefig(f"{power_name}-balance.png")
        plt.close()

        plt.figure()
        plt.plot(Hour,Sheat,'r')
        plt.plot(Hour,Scool,'b')
        plt.plot(Hour,Sbase,'y')
        plt.xlabel("Hour of day")
        plt.ylabel("Temperature sensitivity (MW/degF)")
        plt.legend(['Heating','Cooling','Baseload'])
        plt.title('Load temperature sensitivity')
        plt.grid()
        plt.savefig(f"{power_name}-sensitivity.png")
        plt.close()

    return model


class Model:

    def __init__(self,x,y,n):
        self.bounds = bounds = {1: None, 2: None, 3:([47,52], [56,65])}
        self.model = pwlf.PiecewiseLinFit(x,y)
        self.data = (x,y)
        self.n = n
        self.breaks = breaks = [50,60]
        self.x = X = self.model.fit(n, bounds = bounds[n])
        self.y = Y = self.model.predict(X)
        self.s = S = (Y[1:]-Y[0:-1]) / (X[1:]-X[0:-1])
        self.i = (Y[1:]+Y[0:-1] -S*(X[1:]+X[0:-1])) / 2
        self.t = self.temps(n)


    def __str__(self):
        result = f"{repr(self)}\n    n = {self.n}\n"
        result += f"    x = {self.x}\n"
        result += f"    y = {self.y}\n"
        result += f"    s = {self.s}\n"
        result += f"    i = {self.i}\n"
        result += f"    t = {self.t}\n"
        return result

    def temps(self,n):
        if n == 3:
            Tavg = np.mean(self.x)
        elif n == 2:
            Tavg = self.x[0]
        return Tavg

    def to_dict(self):
        return {"x": self.x, "y": self.y, "s" : self.s, "i" : self.i, "t" : self.t}

    def get_data(self):
        return model.data

    def predict(self,x):
        return self.model.predict(x)


class Model_2:

    def __init__(self,x,y):
        self.model = st.linregress(x,y)
        self.data = (x,y)
        self.x = X = x
        self.y = Y = y
        self.s = slope =  self.model[0]
        self.i = intercept = self.model[1]
        self.t = self.temps()

    def __str__(self):
        result = f"{repr(self)}\n    n = {self.n}\n"
        result += f"    x = {self.x}\n"
        result += f"    y = {self.y}\n"
        result += f"    s = {self.s}\n"
        result += f"    i = {self.i}\n"
        result += f"    t = {self.t}\n"
        return result

    def to_dict(self):
        return {"x": self.x, "y": self.y, "s" : self.s, "i" : self.i, "t" : self.t}

    def temps(self):
        Tavg = (max(self.x) + min(self.x))/2
        return Tavg

    def get_data(self):
        return model.data

    def predict(self,x):
        return self.s * x + self.i

class Model_3:

    def __init__(self,x,y):
        self.data = (x,y)
        self.x = X = x
        self.y = Y = np.ones(len(y))*np.mean(y)

    def __str__(self):
        result = f"{repr(self)}\n    n = {self.n}\n"
        result += f"    x = {self.x}\n"
        result += f"    y = {self.y}\n"

        return result

    def to_dict(self):
        return {"x": self.x, "y": self.y}


    def get_data(self):
        return model.data

    def predict(self,x):
        return self.y


def get_model_1(data, datetime_col, power_col, temperature_col, enduse, dataset,
        skiprows=config.SkipRows,
        ofile=None,
        saveplots=config.SavePlots):

    weather_enduses = {'sensitive': ['Cool', 'Heat'], 'insensitive': ['Process','Vent', 'AirComp', 'Refrig', 'Motors', 'OffEquip', 'Misc', 'ExtLight', 'Cook', 'HotWater', 'IntLight']}
    weather_enduses_rbsa = {'sensitive' : ['cooling', 'heating', 'other', 'hc'], 'insensitive': ['computer', 'dryer', 'entertainment', 'freezer', 'lighting', 'oven', 'plug', 'refrig', 'washer', 'waterheat']}
    btype_dict = {'office': ['LOFF'], 'lodging': ['LODG'], 'commercial': ['AWHS', 'COLL', 'GROC', 'HLTH', 'MISC', 'REFW', 'REST', 'RETL', 'SCHL', 'WRHS', 'AOFF', 'SOFF'], 'residential' : ['RES']}
    def get_keys(dictionary, val):
        for key, value in dictionary.items():
            if val in value:
                return key


    if dataset == 'rbsa':
        weather_enduse_dict = weather_enduses_rbsa
    elif dataset == 'ceus':
        weather_enduse_dict = weather_enduses


    if saveplots:
        fig = plt.figure(figsize=(24,24))
        ax = fig.subplots(8,3).flatten()

    xmin = data["temperature"].min()
    xmax = data["temperature"].max()
    ymin = data["power"].min()
    ymax = data["power"].max()

    hour = list(map(lambda h: get_hours(data,[h]),range(24)))
    model = []
    for h in range(24):

        T = hour[h]["temperature"]
        P = np.array(hour[h]["power"])

        if get_keys(weather_enduse_dict, enduse) == 'sensitive':

            model.append(Model(T,P,2))

        elif get_keys(weather_enduse_dict, enduse) == 'insensitive':
            model.append(Model_2(T, P))
            if model[h].predict(20) < 0 or model[h].predict(90) < 0 :
                model[h] = Model_3(T,P)

        if saveplots:
            ax[h].plot(T,P,'.',ms=0.1,color='blue')
            ax[h].plot(model[h].x,model[h].y,color='black')
            ax[h].set_xlim([xmin,xmax])
            ax[h].set_ylim([ymin,ymax])
            ax[h].set_title(f"Hour {h}")
            ax[h].grid()

    return model


def selftest():
    """
    Run selftest on the module

    The selftest uses the file 'testdata.csv' and prints the following output.

         Pbase   Pheat   Pcool   Tmin  Theat  Tcool  Tmax  Sbase  Sheat  Scool
    Hour
    0    1,779.5 2,667.5 2,560.3 22.9  51.2   61.2   79.8  1.6    -31.4  41.9
    1    1,704.0 2,616.7 2,246.5 22.6  50.7   60.7   75.5  2.3    -32.4  36.9
    2    1,664.1 2,610.3 2,168.5 22.2  50.7   60.7   76.5  2.8    -33.2  31.8
    3    1,657.0 2,669.1 2,106.7 21.4  50.8   60.8   76.2  2.5    -34.5  29.1
    4    1,707.4 2,791.8 2,040.0 20.9  50.8   60.8   73.1  2.6    -36.2  27.1
    5    1,860.0 3,009.3 2,063.1 20.8  51.3   61.3   71.3  2.5    -37.7  20.4
    6    2,101.4 3,350.6 2,281.9 21.2  53.0   63.0   73.6  1.2    -39.3  17.0
    7    2,275.2 3,561.2 2,557.6 20.8  54.2   64.2   81.2  0.3    -38.5  16.6
    8    2,344.9 3,571.4 2,869.2 20.6  53.8   63.8   83.8  0.7    -37.0  26.2
    9    2,383.7 3,549.3 3,064.3 22.5  54.4   64.4   85.9  0.1    -36.5  31.7
    10   2,412.6 3,461.4 3,262.9 25.4  55.2   65.2   88.2  -0.1   -35.1  36.9
    11   2,419.4 3,401.7 3,377.8 26.5  56.0   66.0   91.6  -0.4   -33.3  37.4
    12   2,414.3 3,370.5 3,519.3 27.1  57.0   67.0   94.5  -1.6   -32.0  40.3
    13   2,405.8 3,379.1 3,690.4 26.1  57.5   67.5   98.4  -1.9   -31.0  41.5
    14   2,378.1 3,374.5 4,011.7 25.2  57.8   67.8   105.8 -2.5   -30.6  43.0
    15   2,361.1 3,385.2 4,132.7 24.7  58.2   68.2   106.9 -3.9   -30.6  45.8
    16   2,364.4 3,530.7 4,215.5 24.0  59.1   69.1   107.0 -5.5   -33.2  48.9
    17   2,387.6 3,746.0 4,232.6 23.6  59.8   69.8   106.6 -6.4   -37.6  50.2
    18   2,403.1 3,706.4 4,157.1 23.7  59.7   69.7   105.1 -4.0   -36.1  49.6
    19   2,427.6 3,607.4 4,003.6 23.2  57.2   67.2   101.6 -1.3   -34.7  45.7
    20   2,413.3 3,507.8 3,874.4 22.7  56.2   66.2   97.9  -0.8   -32.7  46.1
    21   2,314.8 3,327.8 3,634.9 22.2  54.5   64.5   91.5  0.3    -31.4  48.9
    22   2,129.6 3,086.1 3,269.4 22.2  52.9   62.9   86.8  0.5    -31.2  47.6
    23   1,934.0 2,853.5 3,009.2 22.2  52.0   62.0   85.3  1.3    -30.9  46.1
    """
    data = load_data(ifile='testdata.csv')
    model = get_model(data,datetime_col=0,power_col=1,temperature_col=2,saveplots=True)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    pd.options.display.float_format = '{:,.1f}'.format
    print(model)

#if __name__ == '__main__':
 #   selftest()

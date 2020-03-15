from pandas import *
from datetime import *
from matplotlib.pyplot import *
from numpy import *
from scipy.stats import *

Tdiff = 10
Tbase = 60
Days = [0,1,2,3,4]
Tmax = 110
Pmin = 0
saveplots = True
datetime_format = '%m/%d/%y %H:%M'
null_value = float('nan')
skiprows = 0

def read_datetime(x,format=datetime_format):
	return datetime.strptime(x,format)

def read_float(x,null=null_value):
	try:
		return float(x)
	except:
		return null_value

def load_data(ifile,datetime,power,temperature,skiprows=skiprows,filter=True,Tmax=Tmax,Pmin=Pmin):
	data = read_csv(ifile, 
			low_memory=False,header=None,skiprows=skiprows,
			index_col=0,converters={datetime:read_datetime,power:read_float,temperature:read_float},
			usecols=[datetime,power,temperature],names=['datetime','power','temperature'])
	if filter:
		data = data[data['temperature']<Tmax]
		data = data[data['power']>Pmin]
	return data

def get_days(data,days):
	return data[data.index.dayofweek.isin(days)]

def get_hours(data,hours):
	return data[data.index.hour.isin(hours)]

def get_baseload(data,Tbase=Tbase,Tdiff=Tdiff,max_iterations=50):
	slope=np.Infinity
	n = 1
	while abs(slope) > 0.1 and n < max_iterations:
		base = data[(data['temperature']-Tbase).abs()<=Tdiff/2]
		temp = array(base['temperature'])
		load = array(base['power'])
		slope, intercept, rvalue, pvalue, stderr = linregress(temp,load)
		Tbase -= slope * 0.1/n
		load = intercept + slope*Tbase
		# print(h,load,slope,Tbase)
		n += 1
	return load, slope, Tbase, base

def get_sensitivity(heating,cooling):
	
	temp = array(heating['temperature'])
	load = array(heating['power'])
	heat_slope, heat_intercept, heat_r_value, heat_p_value, heat_std_err = linregress(temp,load)

	temp = array(cooling['temperature'])
	load = array(cooling['power'])
	cool_slope, cool_intercept, cool_rvalue, cool_pvalue, cool_stderr = linregress(temp,load)

	return heat_slope, cool_slope

def get_model(ifile,datetime,power,temperature,
		skiprows=0,
		ofile=None,
		saveplots=False):
	if not ifile[-4:] == '.csv':
		print(ifile[-4:])
		raise Exception(f"ifile={ifile} is not a valid CSV filename")
	else:
		name = ifile[0:-4]
	if ofile == 'auto':
		ofile = f"{name}-model.csv"
	data = load_data(ifile=ifile,datetime=datetime,power=power,temperature=temperature,skiprows=skiprows)
	days = get_days(data=data,days=[0,1,2,3,4])
	model = {"Hour":[], "Tbal":[], "Load":[], "Base":[], "Heat":[], "Cool":[], "Tmin":[], "Tmax":[]}
	for h in range(0,24):
		hour = get_hours(data=days,hours=[h])
		load, base, Tbal, neither = get_baseload(hour)
		heating = hour[hour['temperature']<Tbal-Tdiff/2]
		cooling = hour[hour['temperature']>Tbal+Tdiff/2]
		heat, cool = get_sensitivity(heating=heating,cooling=cooling)
		Tlo = hour['temperature'].min()
		Thi = hour['temperature'].max()
		model["Hour"].append(h)
		model["Tbal"].append(Tbal)
		model["Load"].append(load)
		model["Base"].append(base)
		model["Heat"].append(heat)
		model["Cool"].append(cool)
		model["Tmin"].append(Tlo)
		model["Tmax"].append(Thi)

		if saveplots:
			figure()
			Theat = Tbal - Tdiff/2
			Tcool = Tbal + Tdiff/2
			Pheat = load + (Tlo-Theat)*heat
			Pcool = load + (Thi-Tcool)*cool
			plot(heating['temperature'],heating['power'],'.r')
			plot(cooling['temperature'],cooling['power'],'.b')
			plot(neither['temperature'],neither['power'],'.y')
			plot([Tlo,Theat,Tcool,Thi],[Pheat,load,load,Pcool],'k')
			grid()
			legend(['Heating','Cooling','Baseload','Profile'],loc=9)
			xlabel('Temperature (degF)')
			ylabel('Load (MW)')
			title(f'Load profile for hour {h}')
			savefig('%s-profile-%02d.png'%(name,h))
			close()

	model = DataFrame(model).set_index("Hour")

	if ofile:
		model.to_csv(ofile)

	if saveplots:

		figure()
		plot(model["Load"],model["Tbal"],'.')
		grid()
		xlabel('Base load (MW)')
		ylabel('Balance temperature (degF)')
		title('Balance temperature vs Base load')
		savefig(f'{name}-balance-load.png')
		close()

		figure()
		plot(model.index,model["Tbal"])
		grid()
		xlabel("Hour of day")
		ylabel("Balance temperature (degF)")
		title(f'Balance temperature (+/- {Tdiff/2} degF)')
		savefig(f"{name}-loadshape.png")
		close()

		figure()
		plot(model.index,model["Load"],'y')
		plot(model.index,model["Load"]+(model["Tmin"]-model["Tbal"]-Tdiff/2)*model["Heat"],'r')
		plot(model.index,model["Load"]+(model["Tmax"]-model["Tbal"]+Tdiff/2)*model["Cool"],'b')
		grid()
		xlabel("Hour of day")
		ylabel('Load (MW)')
		title('Load shapes')
		legend(["Base load","Peak heating","Peak cooling"])
		savefig(f"{name}-balance.png")
		close()

		figure()
		plot(model.index,model["Heat"],'r')
		plot(model.index,model["Cool"],'b')
		plot(model.index,model["Base"],'y')
		xlabel("Hour of day")
		ylabel("Temperature sensitivity (MW/degF)")
		legend(['Heating','Cooling','Baseload'])
		title('Load temperature sensitivity')
		grid()
		savefig(f"{name}-sensitivity.png")
		close()

	return model

def selftest():
	model = get_model(ifile='testdata.csv',datetime=0,power=1,temperature=2,skiprows=1)
	set_option('display.max_columns', None)
	set_option('display.max_rows', None)
	set_option('display.width', None)
	set_option('display.max_colwidth', -1)
	print(model)

if __name__ == '__main__':
	selftest()
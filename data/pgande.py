
import pycurl
from io import BytesIO, StringIO
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


def get_load_profile(date):
	buffer = BytesIO()
	c = pycurl.Curl()
	datename = date.strftime('%Y%m%d')
	c.setopt(c.URL, f'https://www.pge.com/pge_global/forms/mads/profiles/{datename}.dlp')
	c.setopt(c.WRITEDATA, buffer)
	body = c.perform_rs()
	if c.getinfo(pycurl.HTTP_CODE) != 200:
		print(f"ERROR: get_load_profile(date={date}): no data")
		return pd.DataFrame()
	c.close()

	df = pd.read_csv(StringIO(body)).dropna(how='all').transpose()
	df.columns = list(np.array(df[1:2])[0])
	assert(datename == df.index[0])
	df.drop([datename,'Profile','Method'],inplace=True)
	def get_time(date,time):
		t = time.split(':')
		t = (24+int(t[0]))*60 + int(t[1]) - 30
		y = int(date[0:4])
		m = int(date[4:6])
		d = int(date[6:8])
		H = int(t/60) % 24
		M = t % 60
		return datetime(y,m,d,H,M,0)
	df.index = list(map(lambda t: get_time(datename,t),df.index))

	return df

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days+1)):
        yield start_date + timedelta(n)

def get_loads(start,stop,show_progress=False):
	result = pd.DataFrame()
	for date in daterange(start,stop):
		if show_progress:
			print(f"Processing {date}...",flush=True)
		try:
			df = None
			df = get_load_profile(date)
		except Exception as err:
			print(f"ERROR: get_load_profile(date={date}): {err}")
			df = DataFrame()
		try:
			result = result.append(df,sort=True)
		except Exception as err:
			savefile = date.strftime('%Y%m%d-err.csv')
			print(f"ERROR: get_load_profile(date={date}): {err}, saving bad data to {savefile}")
			df.to_csv(savefile)
			pass
	return result

if __name__ == '__main__':
	data = get_loads(datetime(2020,3,1),datetime(2020,3,31),show_progress=True)
	data.to_csv('pge_loads.csv')

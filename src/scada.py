import sys
import csv
import datetime as dt
import numpy as np

def read_datetime(x,format='%m/%d/%y %H:%M'):
	return dt.datetime.strptime(x,format)

def read_timestamp(x,format='%m/%d/%y %H:%M'):
	return dt.datetime.strptime(x,format).timestamp()

def read_float(x,errorvalue=float('nan')):
	try:
		return float(x)
	except:
		if type(errorvalue) is None:
			pass
		return errorvalue

def column_count(ifile):
	with open(ifile,"r") as input:
		reader = csv.reader(input)
		for row in reader:
			return len(row)
	return None

def get_row(ifile,n):
	with open(ifile,"r") as input:
		reader = csv.reader(input)
		m = 0
		for row in reader:
			m += 1
			if n == m:
				return row
	return None

def get_data(ifile,col,
		startrow=6,stoprow=-1,
		indexcol=0,
		namerow=1,skiprows=[],voltrow=None,typerow=None,unitrow=None,
		readindex=read_timestamp,readvalue=read_float,
		errorcall=print,empty='ignore'):
	"""Extract SCADA telemetry data

	Parameters:
		ifile
		col
		startrow
		stoprow
		indexcol
		namerow
		skiprows
		voltrows
		typerow
		unitrow
		errorcall
		empty

	Returns:
		dict
			data (dict) - 
			name (string)
	"""
	result = {'data':{},'name':[],'volt':[],'type':[],'unit':[]}
	with open(ifile,"r") as input:
		reader = csv.reader(input)
		n = 0
		l = 0
		for row in reader:
			n += 1
			try:
				if len(row) == 0:
					if empty == 'ignore':
						continue
					elif empty == 'error':
						errorcall('empty row')
					else:
						raise Exception(f"{ifile}:{n}: empty row")
				elif l > 0 and not len(row) == l and errorcall:
					errorcall(f"row {n} has an incorrect number of fields")
				elif n == namerow:
					for i in col:
						result['name'].append(row[i].strip())
					l = len(row)
				elif n in skiprows:
					continue
				elif n == voltrow:
					for i in col:
						result['volt'].append(readvalue(row[i]))
				elif n == typerow:
					for i in col:
						result['type'].append(row[i].strip())
				elif n == unitrow:
					for i in col:
						result['unit'].append(row[i].strip())
				elif n < startrow:
					continue
				elif stoprow > 0 and n > stoprow:
					break
				elif indexcol == None:
					data = []
					for i in col:
						data.append = readvalue(row[i])
					result['data'][n] = data
				else:
					data = []
					for i in col:
						data.append(readvalue(row[i]))
					result['data'][readindex(row[indexcol])] = data
			except Exception as info:
				errorcall(f"{ifile}:{n}: {info} (value = '{row[i]}')")
	return result

def selftest():
	print(f"Rows count..... {column_count('testdata.csv')}")
	result = get_data('testdata.csv',[1],stoprow=10)
	print(result)

if __name__ == '__main__':
	selftest()

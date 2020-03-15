import csv

def anonymize(ifile,ofile,anon_data={1:[1,-1]},hide_data={2:[0,-1]},anon_prefix="anon",hide_value=''):
	"""Anonymize a CSV file

	Parameters:
		ifile (string) - input file name
		ofile (string) - output file name
		anon_data (dict) - anonymization guide
		hide_data (dict) - masking guide
		anon_prefix (string) - string to use for anonymization
		hide_value (string) - value to use for masking data

	Returns:
		int - number of rows processed
	"""
	with open(ofile,"w") as ocsv:
		writer = csv.writer(ocsv)
		with open(ifile,"r") as icsv:
			reader = csv.reader(icsv)
			n = 1
			f = 0
			a = 0
			h = 0
			for row in reader:
				f += len(row)
				if n in hide_data.keys():
					if hide_data[n][0] < 0: hide_data[n][0] += len(row)+1
					if hide_data[n][1] < 0: hide_data[n][1] += len(row)+1
					for i in range(hide_data[n][0],hide_data[n][1]):
						h += 1
						row[i] = hide_value
				elif n in anon_data.keys():
					if anon_data[n][0] < 0: anon_data[n][0] += len(row)+1
					if anon_data[n][1] < 0: anon_data[n][1] += len(row)+1
					for i in range(anon_data[n][0],anon_data[n][1]):
						a += 1
						row[i] = f"{anon_prefix}{i}"
				writer.writerow(row)
				n += 1
	return {"rows":n,"fields":f,"hidden":h,"anonymized":a}

def selftest():
	ifile = 'testdata.csv'
	ofile = 'anondata.csv'
	print(f"Anonymizing '{ifile}' into '{ofile}'")
	res = anonymize(ifile,ofile)
	print(f"rows scanned........ {res['rows']}")
	print(f"fields scanned...... {res['fields']}")
	print(f"fields hidden....... {res['hidden']}")
	print(f"fields anonymized... {res['anonymized']}")
	print(f"selftest ok")

if __name__ == '__main__':
	selftest()

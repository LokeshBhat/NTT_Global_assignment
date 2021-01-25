import requests
import tabulate
import json


ip = input("Enter the interface name or Enter 'all' to view all the interfaces: ")
ip = ip.strip()

# api-endpoint for getting all the interfaces
if (ip == 'all'):
	URL = "http://localhost:5000/all"

	# sending get request and saving the response as response object
	r = requests.get(url=URL)

	# extracting data in json format
	data = r.json()
	data = data.replace("\'", "\"")
	data = json.loads(data)

	# Conversion to table format
	header = data[0].keys()
	rows = [x.values() for x in data]
	print('\nAll Interface blocks')
	print(tabulate.tabulate(rows, header, tablefmt='grid'))


else:
	# Single interface test
	ip = ip.replace("/","_")
	URL = "http://localhost:5000/all/"+ip

	# sending get request and saving the response as response object
	r = requests.get(url=URL)

	# extracting data in json format
	data = r.json()
	data = data.replace("\'", "\"")
	data = json.loads(data)

	# Conversion to table format
	header = data[0].keys()
	rows = [x.values() for x in data]
	print('\nSingle interface block')
	print(tabulate.tabulate(rows, header, tablefmt='grid'))



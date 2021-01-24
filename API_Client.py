import requests
import tabulate
import json

# api-endpoint
URL = "http://localhost:5000/interface"

# sending get request and saving the response as response object
r = requests.get(url=URL)

# extracting data in json format
data = r.json()
data = data.replace("\'", "\"")
data = json.loads(data)


# Conversion to table format
header = data[0].keys()
rows = [x.values() for x in data]
print('All Interface blocks')
print(tabulate.tabulate(rows, header, tablefmt='grid'))


# Single interface test
URL = "http://localhost:5000/interface/FastEthernet3_0"

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



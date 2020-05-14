'''
FligthsDetector
Pavlo Semchyshyn
'''

import requests
import json

url = "https://api.travelpayouts.com/v1/prices/cheap"

querystring = {"origin":"MOW","destination":"HKT","depart_date":"2020-04-11"}

headers = {'x-access-token': 'a9664d3d8dd5b9242289e5ca43869cf8'}

response = requests.request("GET", url, headers=headers, params=querystring)

data = response.json()

with open("example_data.json", "w") as f:
    json.dump(data, f, indent=4)

print(response.text)
import requests
import json
import pandas as pd


def get_cities_json():
    url = "https://api.travelpayouts.com/data/en/cities.json"
    headers = {'x-access-token': 'a9664d3d8dd5b9242289e5ca43869cf8'}

    response = requests.request("GET", url, headers=headers)
    response = json.loads(response.text)
    with open("iata_cities.json", "w") as file:
        json.dump(response, file, indent=4)
    return pd.DataFrame(response)

def read_cities():
    with open("data_dashapps/iata_cities.json", "r", encoding="utf8") as file:
        data = json.load(file)
    return pd.DataFrame(data)

df = read_cities()

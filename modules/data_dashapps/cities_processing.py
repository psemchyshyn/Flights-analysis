import requests
import json
import pandas as pd
from geopy.distance import distance


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


def calc_distance(origin, destination, process_df):
    origin_place_coor = list(df.loc[df["code"] == origin].values[0][2].values())[:: -1]
    destination_coor = list(df.loc[df["code"] == destination].values[0][2].values())[:: -1]
    base_distance = distance(origin_place_coor, destination_coor)
    process_df.sort_values(by="destination", inplace=True)
    new_df = df[df["code"].isin(process_df["destination"])]
    new_df.sort_values(by="code", inplace=True)
    distances = []
    coordinates = []
    for _, row in new_df.iterrows():
        coor = row["coordinates"]
        if isinstance(coor, dict):
            coor = list(reversed(coor.values()))
            dist = distance(coor, origin_place_coor).km
            distances.append(dist)
            coordinates.append(coor)
        else:
            distances.append(None)
            coordinates.append(None)
    process_df["distance"] = distances
    process_df["coordinates"] = coordinates
    process_df.query("distance <= @base_distance", inplace=True)
    process_df.sort_values(by="distance", inplace=True)
    process_df.drop(["actual", "show_to_affiliates", "trip_class", "number_of_changes", "duration"], axis=1, inplace=True)

df = read_cities()

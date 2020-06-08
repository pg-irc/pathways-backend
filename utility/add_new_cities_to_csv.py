import csv
import json
import requests

def read_algolia_data(algolia_data_path):
    with open(algolia_data_path, 'r') as file:
        return json.loads(file.read())


def parse_csv(csv_path):
    with open(csv_path, mode='r') as file:
        csv_reader = csv.reader(file)
        city_to_latlong = {rows[0]: {'lng': float(rows[1]), 'lat': float(rows[2])} for rows in csv_reader}
        return city_to_latlong

def get_latlong(city):
    url = 'https://geocoder.ca/?locate=' + city + '&json=1'
    response = requests.get(url)
    response_json = response.json()
    if 'error' in response_json:
        return {'lng':0, 'lat':0}
    return {'lng':response_json['longt'], 'lat':response_json['latt']}

def main():

    city_latlong_map = parse_csv('../content/city_latlong.csv')
    algolia_data = read_algolia_data('output_data.json')
    for service in algolia_data:
        city = service['address']['city']
        if city not in city_latlong_map:
            city_latlong = get_latlong(city)
            city_latlong_map[city] = city_latlong

    with open('./cities.csv', 'w') as file:
        for city in city_latlong_map:
            file.write(city)
            file.write(',')
            file.write(str(city_latlong_map[city]['lng']))
            file.write(',')
            file.write(str(city_latlong_map[city]['lat']))
            file.write('\r\n')

main()

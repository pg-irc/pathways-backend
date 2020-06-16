import csv
import sys
import requests
from algolia.helpers import read_algolia_data, parse_cities_csv

# invoke as follows:
# python ./utility/update_csv_with_cities_from_db.py ../content/city_latlong.csv output_data.json new_city_latlong.csv

def get_latlong(city):
    url = 'https://geocoder.ca/?locate=' + city + '&json=1'
    response = requests.get(url)
    response_json = response.json()
    if 'error' in response_json:
        return {'lng':0, 'lat':0}
    return {'lng':response_json['longt'], 'lat':response_json['latt']}

def main():

    if len(sys.argv) < 3:
        print('usage: {} city_latlong.csv output_data.json new_city_latlong.csv'.
              format(sys.argv[0]))
        exit()

    city_latlong_csv_path = sys.argv[1]
    city_latlong_map = parse_cities_csv(city_latlong_csv_path)

    algolia_data_path = sys.argv[2]
    algolia_data = read_algolia_data(algolia_data_path)

    output_csv_path = sys.argv[3]

    for service in algolia_data:
        city = service['address']['city']
        if city not in city_latlong_map:
            city_latlong = get_latlong(city)
            city_latlong_map[city] = city_latlong

    with open(output_csv_path, 'w') as file:
        for city in city_latlong_map:
            file.write(city)
            file.write(',')
            file.write(str(city_latlong_map[city]['lng']))
            file.write(',')
            file.write(str(city_latlong_map[city]['lat']))
            file.write('\r\n')

main()

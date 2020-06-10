from math import sin, cos, sqrt, atan2, radians
import json
import csv

def read_algolia_data(algolia_data_path):
    with open(algolia_data_path, 'r') as file:
        return json.loads(file.read())


def parse_csv(csv_path):
    with open(csv_path, mode='r') as file:
        csv_reader = csv.reader(file)
        city_to_latlong = {rows[0]: {'lat': float(rows[1]), 'lng': float(rows[2])} for rows in csv_reader}
        return city_to_latlong

def get_distance_from_latlong_in_km(lat1, lon1, lat2, lon2):
    radius = 6372.8

    lat1_rad = radians(float(lat1))
    lon1_rad = radians(float(lon1))
    lat2_rad = radians(float(lat2))
    lon2_rad = radians(float(lon2))

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    angle = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    central_angle = 2 * atan2(sqrt(angle), sqrt(1 - angle))

    distance = radius * central_angle
    return distance

def main():

    city_latlong_map = parse_csv('../content/city_latlong.csv')
    algolia_data = read_algolia_data('output_data.json')

    with open('./cities.txt', 'w') as file:
        for service in algolia_data:
            latlong = service['_geoloc']
            city = service['address']['city']
            city_latlong = city_latlong_map[city]
            try:
                distance = get_distance_from_latlong_in_km(latlong['lat'], latlong['lng'], city_latlong['lat'], city_latlong['lng'])
            except ValueError:
                continue
            if distance > 20 and latlong['lat'] != '':
                file.write(service['service_id'])
                file.write(',')
                file.write(str(distance))
                file.write(',')
                file.write(str(latlong['lat']))
                file.write(',')
                file.write(str(latlong['lng']))
                file.write(',')
                file.write(city)
                file.write(',')
                file.write(str(city_latlong['lat']))
                file.write(',')
                file.write(str(city_latlong['lng']))
                file.write('\r\n')

main()

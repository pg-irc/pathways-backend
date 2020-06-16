from math import sin, cos, sqrt, atan2, radians
import csv
import sys
from algolia.helpers import read_algolia_data

# invoke as follows:
# python ./utility/find_out_of_place_services.py ../content/city_latlong.csv output_data.json 20 distant_services.csv

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

    if len(sys.argv) < 4:
        print('usage: {} city_latlong.csv output_data.json distance_threshold distant_services.csv'.
              format(sys.argv[0]))
        exit()

    city_latlong_csv_path = sys.argv[1]
    city_latlong_map = parse_csv(city_latlong_csv_path)

    algolia_data_path = sys.argv[2]
    algolia_data = read_algolia_data(algolia_data_path)

    distance_threshold = float(sys.argv[3])
    output_csv_path = sys.argv[4]

    with open(output_csv_path, 'w') as file:
        for service in algolia_data:
            latlong = service['_geoloc']
            city = service['address']['city']
            city_latlong = city_latlong_map[city]
            try:
                distance = get_distance_from_latlong_in_km(latlong['lat'], latlong['lng'], city_latlong['lat'], city_latlong['lng'])
            except ValueError:
                continue
            if distance > distance_threshold and latlong['lat'] != '':
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

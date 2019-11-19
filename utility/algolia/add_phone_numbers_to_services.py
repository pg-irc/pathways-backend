import csv
import json
import sys


def read_phone_data(phone_data_path):
    result = {}
    with open(phone_data_path) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            location_id = row[0]
            phone_number = row[1]
            phone_number_type_id = row[2]

            if not location_id in result:
                result[location_id] = []
            result[location_id].append({'phone_number': phone_number, 'type': phone_number_type_id})

    return result


def read_algolia_data(algolia_data_path):
    with open(algolia_data_path, 'r') as file:
        return json.loads(file.read())


def set_phone_numbers_on_services(algolia_data, phone_data):
    for service in algolia_data:
        location_id = service['location_id']
        if location_id in phone_data:
            service['phone_numbers'] = phone_data[location_id]
    return algolia_data


def main():

    if len(sys.argv) < 4:
        print('usage: {} phone_data.csv algolia_service_data.json output_data.json'.
              format(sys.argv[0]))
        exit()

    phone_data_path = sys.argv[1]
    phone_data = read_phone_data(phone_data_path)

    algolia_data_path = sys.argv[2]
    algolia_data = read_algolia_data(algolia_data_path)

    algolia_data_with_phones = set_phone_numbers_on_services(algolia_data, phone_data)

    output_data_path = sys.argv[3]
    with open(output_data_path, 'w') as file:
        file.write(json.dumps(algolia_data_with_phones))


main()

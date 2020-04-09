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

            if location_id not in result:
                result[location_id] = []
            result[location_id].append({'phone_number': phone_number, 'type': phone_number_type_id})

    return result


def read_taxonomy_data(taxonomy_data_path):
    result = {}
    with open(taxonomy_data_path) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            service_id = row[0]
            taxonomy_term = row[1]

            if service_id not in result:
                result[service_id] = []
            result[service_id].append(taxonomy_term)
    return result


def read_algolia_data(algolia_data_path):
    with open(algolia_data_path, 'r') as file:
        return json.loads(file.read())


def set_phone_numbers_on_services(algolia_data, phone_data):
    for service in algolia_data:
        location_id = service['location_id']
        if location_id in phone_data:
            service['phone_numbers'] = phone_data[location_id]
        else:
            service['phone_numbers'] = []
    return algolia_data


def set_taxonomy_terms_on_services(algolia_data, taxonomy_data):
    for service in algolia_data:
        service_id = service['service_id']
        if service_id in taxonomy_data:
            service['taxonomy_terms'] = taxonomy_data[service_id]
        else:
            service['taxonomy_terms'] = []
    return algolia_data


def main():

    if len(sys.argv) < 5:
        print('usage: {} phones_data.csv taxonomy_data.csv services.json output_data.json'.
              format(sys.argv[0]))
        exit()

    phone_data_path = sys.argv[1]
    phone_data = read_phone_data(phone_data_path)

    taxonomy_data_path = sys.argv[2]
    taxonomy_data = read_taxonomy_data(taxonomy_data_path)

    algolia_data_path = sys.argv[3]
    algolia_data = read_algolia_data(algolia_data_path)

    algolia_data_with_phones = set_phone_numbers_on_services(algolia_data, phone_data)
    aloglia_data_with_taxonomy = set_taxonomy_terms_on_services(algolia_data_with_phones, taxonomy_data)

    output_data_path = sys.argv[4]
    with open(output_data_path, 'w') as file:
        file.write(json.dumps(aloglia_data_with_taxonomy))


main()

import json
import sys
from helpers import read_phone_data, read_taxonomy_data, read_algolia_data, set_phone_numbers_on_services, set_taxonomy_terms_on_services

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

import random
import copy
from common.testhelpers.random_test_values import an_integer
from bc211.convert_icarol_csv.parser import compute_hash


class Bc211CsvDataBuilder:
    def __init__(self):
        self.data = [self.a_row()]

    def a_row(self):
        row = {}
        row['ResourceAgencyNum'] = ''
        row['PublicName'] = ''
        row['AlternateName'] = ''
        row['AgencyDescription'] = ''
        row['EmailAddressMain'] = ''
        row['WebsiteAddress'] = ''
        row['Phone1Number'] = ''
        row['Phone1Type'] = ''
        return row

    def next_row(self):
        self.data.append(self.a_row())
        return self

    def duplicate_last_row(self):
        the_copy = copy.deepcopy(self.data[-1])
        self.data.append(the_copy)
        return self

    def with_field(self, key, value):
        self.data[-1][key] = value
        return self

    def as_organization(self):
        self.data[-1]['ResourceAgencyNum'] = str(an_integer())
        self.data[-1]['ParentAgencyNum'] = '0'
        return self

    def as_service(self):
        self.data[-1]['ResourceAgencyNum'] = str(an_integer())
        self.data[-1]['ParentAgencyNum'] = str(an_integer(min=1))
        return self

    def get_keys(self):
        keys = [row.keys() for row in self.data]
        flat_keys = [item for sublist in keys for item in sublist]
        unique_keys = {key for key in flat_keys}
        return list(unique_keys)

    def build(self):
        result = []
        shuffled_keys = self.get_keys()
        random.shuffle(shuffled_keys)
        line = ''
        for key in shuffled_keys:
            line += key + ','
        result.append(line)
        for row in self.data:
            line = ''
            for key in shuffled_keys:
                value = row.get(key, '')
                line += value + ','
            result.append(line)
        return result


class TestDataSink:
    def __init__(self):
        self.organizations = []
        self.services = []
        self.locations = []
        self.services_at_location = []
        self.addresses = []
        self.phone_numbers = []
        self.taxonomy_terms = []
        self.services_taxonomy = []

    def write_organization(self, organization):
        self.organizations.append(organization)

    def write_service(self, service, location_id):
        self.services.append(service)
        the_id = compute_hash(service['id'], location_id)
        self.services_at_location.append({'id': the_id, 'service_id': service['id'], 'location_id': location_id})

    def write_location(self, location):
        self.locations.append(location)

    def write_address(self, address):
        self.addresses.append(address)

    def write_phone_number(self, phone_number):
        self.phone_numbers.append(phone_number)

    def write_taxonomy_term(self, terms):
        self.taxonomy_terms.append(terms)

    def write_service_taxonomy_terms(self, service_taxonomy_terms):
        self.services_taxonomy += service_taxonomy_terms

    def first_organization(self):
        return self.organizations[0]

    def first_service(self):
        return self.services[0]

    def first_location(self):
        return self.locations[0]

    def first_address(self):
        return self.addresses[0]

    def second_address(self):
        return self.addresses[1]

    def first_phone_number(self):
        return self.phone_numbers[0]

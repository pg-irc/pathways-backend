import csv
from bc211.csv_import.parser import compute_hash

organization_columns = ['id', 'name', 'alternate_name', 'description', 'email', 'url', 'tax_status', 'tax_id',
                        'year_incorporated', 'legal_status']
service_columns = ['id', 'organization_id', 'program_id', 'name', 'alternate_name', 'description', 'url', 'email',
                   'status', 'interpretation_services', 'application_process', 'wait_time', 'fees', 'accreditations',
                   'licenses', 'taxonomy_ids', 'last_verified_on-x']
location_columns = ['id', 'organization_id', 'name', 'alternate_name', 'description', 'transportation', 'latitude',
                    'longitude']
services_at_location_columns = ['id', 'service_id', 'location_id', 'description']
address_columns = ['id', 'type', 'location_id', 'attention', 'address_1', 'address_2', 'address_3', 'address_4', 'city',
                   'region', 'state_province', 'postal_code', 'country']
phones_columns = ['id', 'location_id', 'service_id', 'organization_id', 'contact_id', 'service_at_location_id',
                  'number', 'extension', 'type', 'language', 'description', 'department']
taxonomy_columns = ['id', 'name', 'parent_id', 'parent_name', 'vocabulary']
services_taxonomy_columns = ['id', 'service_id', 'taxonomy_id', 'taxonomy_detail']


class CsvFileSink:
    def __init__(self, path):
        self.organization_writer = self.make_writer(path, 'organizations', organization_columns)
        self.service_writer = self.make_writer(path, 'services', service_columns)
        self.location_writer = self.make_writer(path, 'location', location_columns)
        self.services_at_location_writer = self.make_writer(path, 'services_at_location', services_at_location_columns)
        self.address_writer = self.make_writer(path, 'addresses', address_columns)
        self.phones_writer = self.make_writer(path, 'phones', phones_columns)
        self.taxonomy_writer = self.make_writer(path, 'taxonomy', taxonomy_columns)
        self.services_taxonomy_writer = self.make_writer(path, 'services_taxonomy', services_taxonomy_columns)

    def make_writer(self, path, filename, columns):
        full_path = path + '/' + filename + '.csv'
        writable_file_handle = open(full_path, 'w')
        writer = csv.writer(writable_file_handle)
        writer.writerow(columns)
        return writer

    def write_organization(self, organization):
        row = [organization.get(column, '') for column in organization_columns]
        self.organization_writer.writerow(row)

    def write_service(self, service, location_id):
        row = [service.get(column, '') for column in service_columns]
        self.service_writer.writerow(row)

        self.write_service_at_location(service, location_id)

    def write_service_at_location(self, service, location_id):
        the_id = compute_hash(service['id'], location_id)
        service_at_location = {'id': the_id, 'service_id': service['id'], 'location_id': location_id}
        row = [service_at_location.get(column, '') for column in services_at_location_columns]
        self.services_at_location_writer.writerow(row)

    def write_location(self, location):
        row = [location.get(column, '') for column in location_columns]
        self.location_writer.writerow(row)

    def write_address(self, address):
        row = [address.get(column, '') for column in address_columns]
        self.address_writer.writerow(row)

    def write_phone_number(self, phone_number):
        row = [phone_number.get(column, '') for column in phones_columns]
        self.phones_writer.writerow(row)

    def write_taxonomy_term(self, terms):
        row = [terms.get(column, '') for column in taxonomy_columns]
        self.taxonomy_writer.writerow(row)

    def write_service_taxonomy_terms(self, service_taxonomy_terms):
        for term in service_taxonomy_terms:
            row = [term.get(column, '') for column in services_taxonomy_columns]
            self.services_taxonomy_writer.writerow(row)

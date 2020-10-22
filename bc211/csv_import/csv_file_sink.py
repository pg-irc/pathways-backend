import csv

organization_columns = ['id', 'name', 'alternate_name', 'description', 'email', 'url', 'tax_status', 'tax_id',
                        'year_incorporated', 'legal_status']


class CsvFileSink:
    def __init__(self, path):
        self.organizations_writer = self.make_writer(path, 'organizations', organization_columns)
        # self.organizations_file = open(self.path_to('services'), 'w')
        # self.organizations_file = open(self.path_to('locations'), 'w')
        # self.organizations_file = open(self.path_to('addresses'), 'w')
        # self.organizations_file = open(self.path_to('phones'), 'w')
        # self.organizations_file = open(self.path_to('taxonomy'), 'w')
        # self.organizations_file = open(self.path_to('services_taxonomy'), 'w')

    def make_writer(self, path, filename, columns):
        full_path = path + '/' + filename + '.csv'
        writable_file_handle = open(full_path, 'w')
        writer = csv.writer(writable_file_handle)
        writer.writerow(columns)
        return writer

    def write_organization(self, organization):
        row = [organization.get(column, '') for column in organization_columns]
        self.organizations_writer.writerow(row)

    def write_service(self, service, location_id):
        pass

    def write_location(self, location):
        pass

    def write_address(self, address):
        pass

    def write_phone_number(self, phone_number):
        pass

    def write_taxonomy_term(self, terms):
        pass

    def write_service_taxonomy_terms(self, service_taxonomy_terms):
        pass

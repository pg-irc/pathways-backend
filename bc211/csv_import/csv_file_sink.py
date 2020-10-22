import csv

organization_columns = ['id', 'name', 'alternate_name', 'description', 'email', 'url', 'tax_status', 'tax_id',
                        'year_incorporated', 'legal_status']


class CsvFileSink:
    def __init__(self, path):
        self.path = path
        self.organizations_writer = csv.writer(open(self.path_to('organizations'), 'w'))
        self.organizations_writer.writerow(organization_columns)
        # self.organizations_file = open(self.path_to('services'), 'w')
        # self.organizations_file = open(self.path_to('locations'), 'w')
        # self.organizations_file = open(self.path_to('addresses'), 'w')
        # self.organizations_file = open(self.path_to('phones'), 'w')
        # self.organizations_file = open(self.path_to('taxonomy'), 'w')
        # self.organizations_file = open(self.path_to('services_taxonomy'), 'w')

    def path_to(self, filename):
        return self.path + '/' + filename + '.csv'

    def write_organization(self, organization):
        values = [organization.get(i, '') for i in organization_columns]
        self.organizations_writer.writerow(values)

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

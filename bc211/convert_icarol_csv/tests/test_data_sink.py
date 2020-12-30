from bc211.convert_icarol_csv.parser import compute_hash


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

class ImportCounters:
    def __init__(self):
        self.organizations_created = 0
        self.locations_created = 0
        self.services_created = 0
        self.service_at_location_count = 0
        self.taxonomy_term_count = 0
        self.address_count = 0
        self.phone_number_types_count = 0
        self.phone_at_location_count = 0

    def count_organization_created(self):
        self.organizations_created += 1

    def count_locations_created(self):
        self.locations_created += 1

    def count_service(self):
        self.services_created += 1

    def count_service_at_location(self):
        self.service_at_location_count += 1

    def count_taxonomy_term(self):
        self.taxonomy_term_count += 1

    def count_address(self):
        self.address_count += 1

    def count_phone_number_types(self):
        self.phone_number_types_count += 1

    def count_phone_at_location(self):
        self.phone_at_location_count += 1

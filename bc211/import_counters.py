class ImportCounters:
    def __init__(self):
        self.organization_count = 0
        self.location_count = 0
        self.service_count = 0
        self.taxonomy_term_count = 0
        self.address_count = 0
        self.phone_number_types_count = 0
        self.phone_at_location_count = 0

    def count_organization(self):
        self.organization_count += 1

    def count_location(self):
        self.location_count += 1

    def count_service(self):
        self.service_count += 1

    def count_taxonomy_term(self):
        self.taxonomy_term_count += 1

    def count_address(self):
        self.address_count += 1

    def count_phone_number_types(self):
        self.phone_number_types_count += 1

    def count_phone_at_location(self):
        self.phone_at_location_count += 1

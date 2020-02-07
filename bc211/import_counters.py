class ImportCounters:
    def __init__(self):
        self.organizations_created = 0
        self.organizations_updated = 0
        self.organizations_deleted = 0
        self.locations_created = 0
        self.locations_updated = 0
        self.locations_deleted = 0
        self.services_created = 0
        self.services_updated = 0
        self.services_deleted = 0
        self.taxonomy_term_count = 0
        self.address_count = 0
        self.phone_number_types_count = 0
        self.phone_at_location_count = 0

    def count_organization_created(self):
        self.organizations_created += 1

    def count_organizations_updated(self):
        self.organizations_updated += 1

    def count_organizations_deleted(self, organizations_deleted):
        self.organizations_deleted += organizations_deleted

    def count_locations_created(self):
        self.locations_created += 1

    def count_locations_updated(self):
        self.locations_updated += 1

    def count_locations_deleted(self, locations_deleted):
        self.locations_deleted += locations_deleted

    def count_service(self):
        self.services_created += 1

    def count_services_updates(self):
        self.services_updated += 1

    def count_services_deleted(self, services_deleted):
        self.services_deleted += services_deleted

    def count_taxonomy_term(self):
        self.taxonomy_term_count += 1

    def count_address(self):
        self.address_count += 1

    def count_phone_number_types(self):
        self.phone_number_types_count += 1

    def count_phone_at_location(self):
        self.phone_at_location_count += 1

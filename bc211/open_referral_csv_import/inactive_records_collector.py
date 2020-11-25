class InactiveRecordsCollector:
    def __init__(self):
        self.inactive_organizations_ids = []
        self.inactive_services_ids = []
        self.inactive_locations_ids = []

    def add_inactive_organization_id(self, organization_id):
        self.inactive_organizations_ids.append(organization_id)

    def add_inactive_service_id(self, service_id):
        self.inactive_services_ids.append(service_id)
    
    def add_inactive_location_id(self, location_id):
        self.inactive_locations_ids.append(location_id)
from bc211.is_inactive import is_inactive


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

    def organization_has_inactive_data(self, organization_id, description):
        if is_inactive(description):
            self.add_inactive_organization_id(organization_id)
            return True
        return False

    def service_has_inactive_data(self, organization_id, service_id, description):
        if is_inactive(description):
            self.add_inactive_service_id(service_id)
            return True
        if self.has_inactive_organization_id(organization_id):
            return True
        return False

    def location_has_inactive_data(self, organization_id, location_id, description):
        if is_inactive(description):
            self.add_inactive_location_id(location_id)
            return True
        if self.has_inactive_organization_id(organization_id):
            return True
        return False

    def has_inactive_organization_id(self, organization_id):
        return organization_id in self.inactive_organizations_ids

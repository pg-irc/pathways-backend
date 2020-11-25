class InactiveRecordsCollector:
    def __init__(self):
        self.inactive_organizations_ids = []

    def add_inactive_organization_id(self, organization_id):
        self.inactive_organizations_ids.append(organization_id)
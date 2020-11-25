def has_inactive_organization_id(organization_id, collector):
    return organization_id in collector.inactive_organizations_ids


def has_inactive_service_id(service_id, collector):
    return service_id in collector.inactive_services_ids


def has_inactive_location_id(location_id, collector):
    return location_id in collector.inactive_locations_ids
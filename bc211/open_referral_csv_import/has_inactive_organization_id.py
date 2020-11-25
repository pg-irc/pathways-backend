def has_inactive_organization_id(organization_id, collector):
    return organization_id in collector.inactive_organizations_ids
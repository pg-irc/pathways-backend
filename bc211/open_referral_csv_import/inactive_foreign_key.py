def has_inactive_location_id(location_id, collector):
    return location_id in collector.inactive_locations_ids

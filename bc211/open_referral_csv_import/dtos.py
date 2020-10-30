from .validate import required_string, optional_string, optional_object, required_float
from bc211.dtos import SpatialLocation


class Organization:
    def __init__(self, **kwargs):
        self.id = required_string('id', kwargs)
        self.name = required_string('name', kwargs)
        self.alternate_name = optional_string('alternate_name', kwargs)
        self.description = optional_string('description', kwargs)
        self.website = optional_string('website', kwargs)
        self.email = optional_string('email', kwargs)


class Service:
    def __init__(self, **kwargs):
        self.id = required_string('id', kwargs)
        self.organization_id = required_string('organization_id', kwargs)
        self.name = required_string('name', kwargs)
        self.alternate_name = optional_string('alternate_name', kwargs)
        self.description = optional_string('description', kwargs)
        self.email = optional_string('email', kwargs)
        self.website = optional_string('website', kwargs)


class Location:
    def __init__(self, **kwargs):
        self.id = required_string('id', kwargs)
        self.organization_id = required_string('organization_id', kwargs)
        self.name = required_string('name', kwargs)
        self.alternate_name = optional_string('alternate_name', kwargs)
        self.description = optional_string('description', kwargs)
        self.spatial_location = optional_object(SpatialLocation, 'spatial_location', kwargs)


class SpatialLocation:
    def __init__(self, **kwargs):
        self.latitude = required_float('latitude', kwargs)
        self.longitude = required_float('longitude', kwargs)


class ServiceAtLocation:
    def __init__(self, **kwargs):
        self.service_id = required_string('service_id', kwargs)
        self.location_id = required_string('location_id', kwargs)

from .validate import required_string, optional_string, optional_object, required_float, required_country_code
from bc211.dtos import SpatialLocation


class SpatialLocation:
    def __init__(self, **kwargs):
        self.latitude = required_float('latitude', kwargs)
        self.longitude = required_float('longitude', kwargs)


class ServiceAtLocation:
    def __init__(self, **kwargs):
        self.service_id = required_string('service_id', kwargs)
        self.location_id = required_string('location_id', kwargs)


class Address:
    def __init__(self, **kwargs):
        self.type = required_string('type', kwargs)
        self.location_id = required_string('location_id', kwargs)
        self.attention = optional_string('attention', kwargs)
        self.address = optional_string('address', kwargs)
        self.city = required_string('city', kwargs)
        self.state_province = optional_string('state_province', kwargs)
        self.postal_code = optional_string('postal_code', kwargs)
        self.country = required_country_code('country', kwargs)
        
        

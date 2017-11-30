from bc211 import validators

class ParserResult:
    organizations = []
    service_providers = []

class Organization:
    def __init__(self, id, name, description, website, email):
        self.id = id
        self.name = name
        self.description = description
        self.website = website
        self.email = email

class ServiceProvider:
    def __init__(self, name, description, spatial_location):
        self.name = name
        self.description = description
        self.spatial_location = spatial_location

class SpatialLocation:
    def __init__(self, latitude, longitude):
        self.latitude = validators.validate_float(latitude)
        self.longitude = validators.validate_float(longitude)

from human_services.locations import models
from common.testhelpers.random_test_values import a_string, a_float

class LocationBuilder:
    def __init__(self, organization):
        self.location_id = a_string()
        self.organization = organization
        self.name = a_string()
        self.latitude = a_float()
        self.longitude = a_float()
        self.description = a_string()

    def with_id(self, location_id):
        self.location_id = location_id
        return self

    def with_name(self, name):
        self.name = name
        return self

    def with_latitude(self, latitude):
        self.latitude = latitude
        return self

    def with_longitude(self, longitude):
        self.longitude = longitude
        return self

    def with_description(self, description):
        self.description = description
        return self

    def build(self):
        result = models.Location()
        result.id = self.location_id
        result.name = self.name
        result.organization = self.organization
        result.latitude = self.latitude
        result.longitude = self.longitude
        result.description = self.description
        return result

    def create(self):
        result = self.build()
        result.save()
        return result

class ServiceLocationBuilder:
    def __init__(self, service, location):
        self.service = service
        self.location = location

    def build(self):
        result = models.ServiceAtLocation()
        result.service = self.service
        result.location = self.location
        return result

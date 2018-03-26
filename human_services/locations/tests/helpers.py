from common.testhelpers.random_test_values import a_string, a_point
from django.contrib.gis.geos import Point
from human_services.locations.models import Location


class LocationBuilder:
    def __init__(self, organization):
        self.location_id = a_string()
        self.organization = organization
        self.name = a_string()
        self.point = a_point()
        self.description = a_string()

    def with_id(self, location_id):
        self.location_id = location_id
        return self

    def with_name(self, name):
        self.name = name
        return self

    def with_point(self, latitude, longitude):
        self.point = Point(latitude, longitude)
        return self

    def with_description(self, description):
        self.description = description
        return self

    def build(self):
        result = Location()
        result.id = self.location_id
        result.name = self.name
        result.organization = self.organization
        result.point = self.point
        result.description = self.description
        return result

    def create(self):
        result = self.build()
        result.save()
        return result

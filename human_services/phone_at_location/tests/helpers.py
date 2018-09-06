from common.testhelpers.random_test_values import a_string
from human_services.phone_at_location.models import PhoneNumberType, PhoneAtLocation
from human_services.locations.tests.helpers import LocationBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder


class PhoneAtLocationBuilder:
    def __init__(self):
        self.location = LocationBuilder(OrganizationBuilder().build()).build()
        self.phone_number_type = a_string()
        self.phone_number = a_string()

    def with_location(self, location):
        self.location = location
        return self

    def with_phone_number_type(self, phone_number_type):
        self.phone_number_type = phone_number_type
        return self

    def with_phone_number(self, phone_number):
        self.phone_number = phone_number
        return self

    def build(self):
        phone_number = PhoneAtLocation()
        phone_number.location = self.location
        phone_number.phone_number_type = self.phone_number_type
        phone_number.phone_number = self.phone_number
        return phone_number

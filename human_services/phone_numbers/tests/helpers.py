from common.testhelpers.random_test_values import a_string
from human_services.phone_numbers.models import PhoneNumberType, PhoneNumber
from human_services.locations.tests.helpers import LocationBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder


class PhoneNumberTypeBuilder:
    def __init__(self):
        self.id = a_string()

    def with_id(self, type_id):
        self.id = type_id
        return self

    def build(self):
        address_type = PhoneNumberType()
        address_type.id = self.id
        return address_type

class PhoneNumberBuilder:
    def __init__(self):
        self.location = LocationBuilder(OrganizationBuilder().build()).build()
        self.phone_number_type = PhoneNumberTypeBuilder().build()
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
        phone_number = PhoneNumber()
        phone_number.location = self.location
        phone_number.phone_number_type = self.phone_number_type
        phone_number.phone_number = self.phone_number
        return phone_number

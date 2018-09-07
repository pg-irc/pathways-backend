from common.testhelpers.random_test_values import a_string, a_phone_number
from human_services.phone_at_location.models import PhoneNumberType, PhoneAtLocation


class PhoneAtLocationBuilder:
    def __init__(self, location):
        self.location = location
        self.phone_number_type = PhoneNumberType(id=a_string())
        self.phone_number = a_phone_number()

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

    def create(self):
        self.location.save()
        self.phone_number_type.save()
        result = self.build()
        result.save()
        return result

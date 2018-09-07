from django.test import TestCase
from django.core import exceptions
from common.testhelpers.random_test_values import a_string
from common.testhelpers.database import validate_save_and_reload
from human_services.phone_at_location.models import PhoneNumberType
from human_services.phone_at_location.tests.helpers import PhoneAtLocationBuilder
from human_services.locations.tests.helpers import LocationBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder


class TestPhoneAtLocationModel(TestCase):

    def test_has_location_field(self):
        location = LocationBuilder(OrganizationBuilder().build()).build()
        phone_at_location = PhoneAtLocationBuilder(location).build()
        phone_at_location_from_db = validate_save_and_reload(phone_at_location)
        self.assertEqual(phone_at_location_from_db.location, location)

    def test_has_phone_number_type_field(self):
        location = LocationBuilder(OrganizationBuilder().build()).build()
        phone_number_type = PhoneNumberType(id=a_string())
        phone_at_location = PhoneAtLocationBuilder(location).with_phone_number_type(phone_number_type).build()
        phone_at_location_from_db = validate_save_and_reload(phone_at_location)
        self.assertEqual(phone_at_location_from_db.phone_number_type, phone_number_type)

    def test_has_phone_number_field(self):
        location = LocationBuilder(OrganizationBuilder().build()).build()
        phone_number = a_string()
        phone_at_location = PhoneAtLocationBuilder(location).with_phone_number(phone_number).build()
        phone_at_location_from_db = validate_save_and_reload(phone_at_location)
        self.assertEqual(phone_at_location_from_db.phone_number, phone_number)

from django.test import TestCase
from django.core import exceptions
from common.testhelpers.random_test_values import a_string
from common.testhelpers.database import validate_save_and_reload
from human_services.phone_at_location.tests.helpers import PhoneNumberTypeBuilder, PhoneAtLocationBuilder
from human_services.locations.tests.helpers import LocationBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder

class TestPhoneNumberTypeModel(TestCase):

    def test_has_id_field(self):
        type_id = a_string()
        phone_number_type = PhoneNumberTypeBuilder().with_id(type_id).build()
        phone_number_type_from_db = validate_save_and_reload(phone_number_type)
        self.assertEqual(phone_number_type_from_db.id, type_id)

class TestPhoneAtLocationModel(TestCase):

    def test_has_location_field(self):
        location = LocationBuilder(OrganizationBuilder().build()).build()
        phone_number = PhoneAtLocationBuilder().with_location(location).build()
        phone_number_from_db = validate_save_and_reload(phone_number)
        self.assertEqual(phone_number_from_db.location, location)

    def test_has_phone_number_type_field(self):
        phone_number_type = PhoneNumberTypeBuilder().build()
        phone_number = PhoneAtLocationBuilder().with_phone_number_type(phone_number_type).build()
        phone_number_from_db = validate_save_and_reload(phone_number)
        self.assertEqual(phone_number_from_db.phone_number_type, phone_number_type)

    def test_has_phone_number_field(self):
        phone_number = a_string()
        phone_number = PhoneAtLocationBuilder().with_phone_number(phone_number).build()
        phone_number_from_db = validate_save_and_reload(phone_number)
        self.assertEqual(phone_number_from_db.phone_number, phone_number)

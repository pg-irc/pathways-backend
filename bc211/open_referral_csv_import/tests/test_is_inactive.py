from django.test import TestCase
from bc211.open_referral_csv_import.is_inactive import is_inactive

class IsInactiveTests(TestCase):
    def test_can_detect_BC211_convention_for_making_records_inactive_when_DEL_is_uppercase(self):
        description = 'DEL15Community hall, used for various programs. Also available for rent. Seasonal hours; check website.'
        self.assertTrue(is_inactive(description))
    
    def test_can_detect_BC211_convention_for_making_records_inactive_when_DEL_has_lowercase_characters(self):
        description = 'Del15Community hall, used for various programs. Also available for rent. Seasonal hours; check website.'
        self.assertTrue(is_inactive(description))
    
    def test_can_return_false_when_description_is_not_inactive(self):
        description = 'Delivers settlement services'
        self.assertFalse(is_inactive(description))
from django.test import TestCase
from rest_framework import status
from bc211 import version


class TestVersion(TestCase):

    def test_get_version_from_api(self):
        self.bc211_version_string = version.get_version_string()
        url = '/bc211version/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode("utf-8"), self.bc211_version_string)
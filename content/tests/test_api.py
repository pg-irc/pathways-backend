from common.testhelpers.database import validate_save_and_reload
from common.testhelpers.random_test_values import a_string
from content.tests.helpers import AlertBuilder
from rest_framework import test as rest_test
from rest_framework import status

class ContentApiTests(rest_test.APITestCase):
    def setUp(self):
        self.data = {
            "id": a_string(),
            "name": a_string(),
            "description": a_string()
        }

    def test_can_get_alerts(self):
        AlertBuilder().create()
        AlertBuilder().create()
        url = '/v1/alerts/en/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_alert(self):
        alert = AlertBuilder().create()
        url = '/v1/alerts/en/{0}/'.format(alert.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], alert.id)

    def test_no_response_if_no_locale(self):
        url = '/v1/alerts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_post(self):
        url = '/v1/alerts/en/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_put(self):
        alert = AlertBuilder().create()
        url = '/v1/alerts/en/{0}/'.format(alert.pk)
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete(self):
        alert = AlertBuilder().create()
        url ='/v1/alerts/en/{0}/'.format(alert.pk)
        response = self.client.delete(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_return_result_in_specific_locale(self):
        alert = AlertBuilder().build()

        self.set_title_in_language(alert, 'en', 'Title')
        self.set_title_in_language(alert, 'fr', 'Titre')

        self.set_description_in_language(alert, 'en', 'Description')
        self.set_description_in_language(alert, 'fr', 'La description')
        alert_from_db = validate_save_and_reload(alert)

        url = '/v1/alerts/fr/{0}/'.format(alert_from_db.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'Titre')
        self.assertEqual(response.json()['description'], 'La description')

        url = '/v1/alerts/en/{0}/'.format(alert_from_db.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'Title')
        self.assertEqual(response.json()['description'], 'Description')

    def set_title_in_language(self, alert, language, text):
        alert.set_current_language(language)
        alert.title = text

    def set_description_in_language(self, alert, language, text):
        alert.set_current_language(language)
        alert.description = text
from rest_framework import test as rest_test
from rest_framework import status
from human_services.locations.tests.helpers import LocationBuilder, ServiceLocationBuilder
from human_services.locations.models import Location, LocationAddress
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.addresses.tests.helpers import AddressBuilder
from human_services.addresses.models import Address, AddressType
from human_services.services.tests.helpers import ServiceBuilder
from common.testhelpers.random_test_values import a_float
from django.contrib.gis.geos import Point


class LocationsApiTests(rest_test.APITestCase):
    def setUp(self):
        self.organization_id = 'the_organization_id'
        self.organization = OrganizationBuilder().with_id(self.organization_id).build()
        self.organization.save()
        self.data = {
            'id': 'the_location_id',
            'name': 'the name',
            'organization_id': self.organization_id,
            'description': 'the description'
        }

    def test_can_get_locations(self):
        LocationBuilder(self.organization).with_id('First').create()
        LocationBuilder(self.organization).with_id('Second').create()
        url = '/v1/locations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_location(self):
        location = LocationBuilder(self.organization).with_description('The description').build()
        location.save()
        url = '/v1/locations/{0}/'.format(location.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], 'The description')

    def test_cannot_post(self):
        url = '/v1/locations/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_put(self):
        location = LocationBuilder(self.organization).build()
        location.save()
        url = '/v1/locations/{0}/'.format(location.pk)
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete(self):
        location = LocationBuilder(self.organization).build()
        location.save()
        url = '/v1/locations/{0}/'.format(location.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_get_locations_for_organization(self):
        LocationBuilder(self.organization).with_id('First').create()
        LocationBuilder(self.organization).with_id('Second').create()
        url = '/v1/organizations/{0}/locations/'.format(self.organization_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_location_for_organization(self):
        location = LocationBuilder(self.organization).with_description('The description').build()
        location.save()
        url = '/v1/organizations/{0}/locations/{1}/'.format(self.organization_id, location.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], 'The description')

    def test_cannot_post_to_organization(self):
        url = '/v1/organizations/{0}/locations/'.format(self.organization_id)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_put_to_organization(self):
        location = LocationBuilder(self.organization).build()
        location.save()
        url = '/v1/organizations/{0}/locations/{1}/'.format(self.organization_id, location.pk)
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete_on_organization(self):
        location = LocationBuilder(self.organization).build()
        location.save()
        url = '/v1/organizations/{0}/locations/{1}/'.format(self.organization_id, location.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def location_has_address_of_type(self, address_type_id):
        LocationBuilder(self.organization).create()
        AddressBuilder().create()
        LocationAddress(
            location=Location.objects.first(),
            address=Address.objects.first(),
            address_type=AddressType.objects.get(pk=address_type_id)
        ).save()
        url = '/v1/locations/'
        response = self.client.get(url)
        location_addresses = response.json()[0]['location_addresses']
        self.assertEqual(location_addresses[0]['address_type'], address_type_id)

    def test_has_physical_address(self):
        self.location_has_address_of_type('physical_address')

    def test_has_postal_address(self):
        self.location_has_address_of_type('postal_address')

    def test_has_point_values(self):
        point = Point(a_float(), a_float())
        LocationBuilder(self.organization).with_point(point).create()
        url = '/v1/locations/'
        response = self.client.get(url)
        self.assertEqual(response.json()[0]['latitude'], point.x)
        self.assertEqual(response.json()[0]['longitude'], point.y)

    def test_point_values_instantiate_a_point(self):
        LocationBuilder(self.organization).create()
        url = '/v1/locations/'
        response = self.client.get(url)
        # This will throw one of a few various exceptions (causing test failure)
        # if parsing the values fails
        latitude = float(response.json()[0]['latitude'])
        longitude = float(response.json()[0]['longitude'])
        Point(latitude, longitude)

class ServiceAtLocationProximityFilterTests(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()
        self.service = ServiceBuilder(self.organization).create()

    def test_200_response_when_proximity_includes_plus(self):
        url = '/v1/services_at_location/?proximity=+11.1111,+222.2222'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_200_response_when_proximity_excludes_plus(self):
        url = '/v1/services_at_location/?proximity=11.1111,-222.2222'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_400_response_when_proximity_has_one_value(self):
        url = '/v1/services_at_location/?proximity=+11.1111'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_400_response_when_proximity_has_more_than_two_values(self):
        url = '/v1/services_at_location/?proximity=+11.1111,-222.2222,333.3333'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_400_response_when_proximity_uses_none_comma_separator(self):
        url = '/v1/services_at_location/?proximity=+11.1111&-222.2222'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_400_response_when_proximity_to_cannot_represent_a_point(self):
        url = '/v1/services_at_location/?proximity=foo,bar'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_order_by_proximity(self):
        vancouver_location = (LocationBuilder(self.organization)
                              .with_name('Vancouver')
                              .with_point(Point(49.246292, -123.116226)).create())
        chilliwack_location = (LocationBuilder(self.organization)
                              .with_name('Chilliwack')
                              .with_point(Point(49.157940, -121.951467)).create())
        kamloops_location = (LocationBuilder(self.organization)
                              .with_name('Kamloops')
                              .with_point(Point(50.674522, -120.327268)).create())
        salmon_arm_location = (LocationBuilder(self.organization)
                              .with_name('Salmon Arm')
                              .with_point(Point(50.700103, -119.283844)).create())
        ServiceLocationBuilder(self.service, vancouver_location).create()
        ServiceLocationBuilder(self.service, chilliwack_location).create()
        ServiceLocationBuilder(self.service, kamloops_location).create()
        ServiceLocationBuilder(self.service, salmon_arm_location).create()
        near_chilliwack_services_url = '{0}{1},{2}'.format('/v1/services_at_location/?proximity=',
                                                           chilliwack_location.point.x,
                                                           chilliwack_location.point.y)
        response = self.client.get(near_chilliwack_services_url)
        json = response.json()

        self.assertEqual(json[0]['location_name'], chilliwack_location.name)
        self.assertEqual(json[1]['location_name'], vancouver_location.name)
        self.assertEqual(json[2]['location_name'], kamloops_location.name)
        self.assertEqual(json[3]['location_name'], salmon_arm_location.name)

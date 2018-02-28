from rest_framework import test as rest_test
from rest_framework import status
from human_services.locations.tests.helpers import LocationBuilder, ServiceLocationBuilder
from human_services.locations.models import Location, LocationAddress
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.addresses.tests.helpers import AddressBuilder
from human_services.addresses.models import Address, AddressType
from human_services.services.tests.helpers import ServiceBuilder
from human_services.taxonomies.tests.helpers import TaxonomyTermBuilder
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
        latitude = float(response.json()[0]['latitude'])
        longitude = float(response.json()[0]['longitude'])
        Point(latitude, longitude)

class ServicesAtLocationApiTests(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()
        self.service = ServiceBuilder(self.organization).create()

    def create_two_service_at_locations(self):
        first_service = ServiceBuilder(self.organization).with_name('First Service').create()
        first_location = LocationBuilder(self.organization).with_name('First Location').create()
        second_service = ServiceBuilder(self.organization).with_name('Second Service').create()
        second_location = LocationBuilder(self.organization).with_name('Second Location').create()
        return [
            ServiceLocationBuilder(first_service, first_location).create(),
            ServiceLocationBuilder(second_service, second_location).create(),
        ]

    def test_200_response_when_proximity_includes_plus(self):
        url = '/v1/services_at_location/?proximity=+11.1111,+222.2222'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_200_response_when_proximity_excludes_plus(self):
        url = '/v1/services_at_location/?proximity=11.1111,-222.2222'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_order_by_proximity(self):
        first_location = (LocationBuilder(self.organization)
                              .with_name('First')
                              .with_point(Point(0, 0)).create())
        second_location = (LocationBuilder(self.organization)
                              .with_name('Second')
                              .with_point(Point(10, 10)).create())
        third_location = (LocationBuilder(self.organization)
                              .with_name('Third')
                              .with_point(Point(25, 25)).create())
        fourth_location = (LocationBuilder(self.organization)
                              .with_name('Fourth')
                              .with_point(Point(30, 30)).create())

        ServiceLocationBuilder(self.service, first_location).create()
        ServiceLocationBuilder(self.service, second_location).create()
        ServiceLocationBuilder(self.service, third_location).create()
        ServiceLocationBuilder(self.service, fourth_location).create()

        at_second_location_services_url = ('/v1/services_at_location/?proximity={0},{1}'
                                            .format(second_location.point.x, second_location.point.y))

        response = self.client.get(at_second_location_services_url)
        json = response.json()
        self.assertEqual(json[0]['location_name'], second_location.name)
        self.assertEqual(json[1]['location_name'], first_location.name)
        self.assertEqual(json[2]['location_name'], third_location.name)
        self.assertEqual(json[3]['location_name'], fourth_location.name)

    def test_can_full_text_search(self):
        service_at_locations = self.create_two_service_at_locations()
        expected_service_at_location = service_at_locations[1]
        response = self.client.get('/v1/services_at_location/?search=sec')
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location_name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service_name'], expected_service_at_location.service.name)

    def test_can_filter_by_location_id(self):
        service_at_locations = self.create_two_service_at_locations()
        expected_service_at_location = service_at_locations[0]
        location_id = expected_service_at_location.location.id
        response = (self.client.get('/v1/locations/{0}/services_at_location/'
                                    .format(location_id)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location_name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service_name'], expected_service_at_location.service.name)

    def test_can_filter_by_location_id_and_service_id(self):
        service_at_locations = self.create_two_service_at_locations()
        expected_service_at_location = service_at_locations[0]
        location_id = expected_service_at_location.location.id
        service_id = expected_service_at_location.service.id
        response = (self.client.get('/v1/locations/{0}/services/{1}/services_at_location/'
                                    .format(location_id, service_id)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location_name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service_name'], expected_service_at_location.service.name)

    def test_can_filter_by_service_id(self):
        service_at_locations = self.create_two_service_at_locations()
        expected_service_at_location = service_at_locations[0]
        service_id = expected_service_at_location.service.id
        response = (self.client.get('/v1/services/{0}/services_at_location/'
                                    .format(service_id)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location_name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service_name'], expected_service_at_location.service.name)

    def test_can_filter_by_service_id_and_location_id(self):
        service_at_locations = self.create_two_service_at_locations()
        expected_service_at_location = service_at_locations[0]
        service_id = expected_service_at_location.service.id
        location_id = expected_service_at_location.location.id
        response = (self.client.get('/v1/services/{0}/locations/{1}/services_at_location/'
                                    .format(service_id, location_id)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location_name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service_name'], expected_service_at_location.service.name)

    def test_can_page(self):
        service_at_locations = self.create_two_service_at_locations()
        expected_service_at_location = service_at_locations[1]
        response = self.client.get('/v1/services_at_location/?per_page=1&page=2')
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location_name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service_name'], expected_service_at_location.service.name)

    def test_can_filter_by_taxonomy(self):
        taxonomy_terms = [TaxonomyTermBuilder().create(), TaxonomyTermBuilder().create()]
        service = ServiceBuilder(self.organization).with_taxonomy_terms(taxonomy_terms).create()
        location = LocationBuilder(self.organization).create()
        expected_service_at_location = ServiceLocationBuilder(service,location).create()
        response = (self.client.get('/v1/services_at_location/?taxonomy_terms={0}.{1}'
                                    .format(taxonomy_terms[0].taxonomy_id, taxonomy_terms[0].name)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location_name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service_name'], expected_service_at_location.service.name)

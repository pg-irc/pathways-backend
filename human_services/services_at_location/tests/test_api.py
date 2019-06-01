from rest_framework import test as rest_test
from rest_framework import status
from human_services.locations.tests.helpers import LocationBuilder
from human_services.services_at_location.tests.helpers import ServiceAtLocationBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from human_services.locations.models import ServiceAtLocation
from search.models import TaskServiceSimilarityScore
from newcomers_guide.tests.helpers import create_topics
from taxonomies.tests.helpers import TaxonomyTermBuilder
from common.testhelpers.random_test_values import a_float
from django.contrib.gis.geos import Point


class ServicesAtLocationApiTests(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()
        self.service = ServiceBuilder(self.organization).create()
        self.location = LocationBuilder(self.organization).create()

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
                          .with_long_lat(0, 0).create())
        second_location = (LocationBuilder(self.organization)
                           .with_name('Second')
                           .with_long_lat(10, 10).create())
        third_location = (LocationBuilder(self.organization)
                          .with_name('Third')
                          .with_long_lat(25, 25).create())
        fourth_location = (LocationBuilder(self.organization)
                           .with_name('Fourth')
                           .with_long_lat(30, 30).create())

        ServiceAtLocation.objects.create(service=self.service, location=first_location)
        ServiceAtLocation.objects.create(service=self.service, location=second_location)
        ServiceAtLocation.objects.create(service=self.service, location=third_location)
        ServiceAtLocation.objects.create(service=self.service, location=fourth_location)

        at_second_location_services_url = ('/v1/services_at_location/?proximity={0},{1}'
                                           .format(second_location.point.x,
                                                   second_location.point.y))

        response = self.client.get(at_second_location_services_url)
        json = response.json()
        self.assertEqual(json[0]['location']['name'], second_location.name)
        self.assertEqual(json[1]['location']['name'], first_location.name)
        self.assertEqual(json[2]['location']['name'], third_location.name)
        self.assertEqual(json[3]['location']['name'], fourth_location.name)

    def test_proximity_sorts_in_km_not_in_degrees(self):
        # using points far north where one degree distance east/west is
        # much shorter in km than one degree distance north/south
        origin = Point(-34.515754, 83.561941)
        west_by_94_km = Point(-41.960183, 83.540722)
        south_by_101_km = Point(-34.845335, 82.655271)

        origin_location = LocationBuilder(self.organization).with_point(origin).create()
        location_101km_away = LocationBuilder(self.organization).with_point(south_by_101_km).create()
        location_94km_away = LocationBuilder(self.organization).with_point(west_by_94_km).create()

        ServiceAtLocation.objects.create(service=self.service, location=origin_location)
        ServiceAtLocation.objects.create(service=self.service, location=location_101km_away)
        ServiceAtLocation.objects.create(service=self.service, location=location_94km_away)

        url_with_proximity_to_origin = ('/v1/services_at_location/?proximity={0},{1}'
                                        .format(origin.x, origin.y))

        response = self.client.get(url_with_proximity_to_origin)
        json = response.json()
        self.assertEqual(json[0]['location']['name'], origin_location.name)
        self.assertEqual(json[1]['location']['name'], location_94km_away.name)
        self.assertEqual(json[2]['location']['name'], location_101km_away.name)

    def test_can_filter_by_proximity(self):
        origin_location = LocationBuilder(self.organization).with_long_lat(0, 0).create()
        near_location = LocationBuilder(self.organization).with_long_lat(0.1, 0).create()
        far_location = LocationBuilder(self.organization).with_long_lat(1.0, 0).create()

        ServiceAtLocation.objects.create(service=self.service, location=origin_location)
        ServiceAtLocation.objects.create(service=self.service, location=near_location)
        ServiceAtLocation.objects.create(service=self.service, location=far_location)

        url_with_user_location = ('/v1/services_at_location/?user_location={0},{1}'
                                  .format(origin_location.point.x, origin_location.point.y))

        response = self.client.get(url_with_user_location)
        names_in_response = [row['location']['name'] for row in response.json()]

        self.assertEqual(len(names_in_response), 2)
        self.assertIn(origin_location.name, names_in_response)
        self.assertIn(near_location.name, names_in_response)

    def test_proximity_filter_excludes_points_more_than_25km_away(self):
        origin = Point(-123.060015, 49.270545)
        point_24km_away = Point(-122.729581, 49.260617)
        point_26km_away = Point(-122.701997, 49.260414)

        origin_location = LocationBuilder(self.organization).with_point(origin).create()
        near_location = LocationBuilder(self.organization).with_point(point_24km_away).create()
        far_location = LocationBuilder(self.organization).with_point(point_26km_away).create()

        ServiceAtLocation.objects.create(service=self.service, location=origin_location)
        ServiceAtLocation.objects.create(service=self.service, location=near_location)
        ServiceAtLocation.objects.create(service=self.service, location=far_location)

        url_with_user_location = ('/v1/services_at_location/?user_location={0},{1}'
                                  .format(origin_location.point.x, origin_location.point.y))

        response = self.client.get(url_with_user_location)
        names_in_response = [row['location']['name'] for row in response.json()]

        self.assertEqual(len(names_in_response), 2)
        self.assertIn(origin_location.name, names_in_response)
        self.assertIn(near_location.name, names_in_response)

    def set_service_similarity_score(self, topic_id, service_id, similarity_score):
        TaskServiceSimilarityScore.objects.create(
            task_id=topic_id,
            service_id=service_id,
            similarity_score=similarity_score
        )

    def test_can_order_by_similarity_to_task(self):
        topic_id = 'the-topic-id'
        create_topics([topic_id])

        similar_service = ServiceBuilder(self.organization).with_location(self.location).create()
        dissimilar_service = ServiceBuilder(self.organization).with_location(self.location).create()

        self.set_service_similarity_score(topic_id, similar_service.id, 0.9)
        self.set_service_similarity_score(topic_id, dissimilar_service.id, 0.1)

        url = '/v1/services_at_location/?related_to_topic={0}'.format(topic_id)
        json = self.client.get(url).json()

        self.assertEqual(len(json), 2)
        self.assertEqual(json[0]['service']['name'], similar_service.name)
        self.assertEqual(json[1]['service']['name'], dissimilar_service.name)

    def test_does_not_return_unrelated_services(self):
        topic_id = 'the-topic-id'
        create_topics([topic_id])
        related_service = ServiceBuilder(self.organization).with_location(self.location).create()
        self.set_service_similarity_score(topic_id, related_service.id, a_float())

        unrelated_service = ServiceBuilder(self.organization).with_location(self.location).create()

        url = '/v1/services_at_location/?related_to_topic={0}'.format(topic_id)
        json = self.client.get(url).json()

        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['service']['name'], related_service.name)

    def test_orders_by_task_passed_to_the_query(self):
        task_passed_to_query = 'the-topic-id'
        task_to_ignore = 'some-other-topic'
        create_topics([task_passed_to_query, task_to_ignore])

        similar_service = ServiceBuilder(self.organization).with_location(self.location).create()
        dissimilar_service = ServiceBuilder(self.organization).with_location(self.location).create()

        lower_score = 0.1
        low_score = 0.2
        high_score = 0.8
        higher_score = 0.9

        self.set_service_similarity_score(task_passed_to_query, similar_service.id, high_score)
        self.set_service_similarity_score(task_passed_to_query, dissimilar_service.id, low_score)

        # Test verifies that these scores are ignored,
        # if they were considered then dissimilar_service would be returned as the first element
        self.set_service_similarity_score(task_to_ignore, similar_service.id, lower_score)
        self.set_service_similarity_score(task_to_ignore, dissimilar_service.id, higher_score)

        url = '/v1/services_at_location/?related_to_topic={0}'.format(task_passed_to_query)
        json = self.client.get(url).json()

        self.assertEqual(len(json), 2)
        self.assertEqual(json[0]['service']['name'], similar_service.name)
        self.assertEqual(json[1]['service']['name'], dissimilar_service.name)

    def test_orders_poor_match_close_by_before_good_match_further_away(self):
        topic_id = 'the-topic-id'
        create_topics([topic_id])

        latitude = 0
        user_longitude = 0
        near_longitude = 0.0001
        far_longitude = 0.0002

        far_location = (LocationBuilder(self.organization).
                        with_long_lat(far_longitude, latitude).
                        create())
        far_service = (ServiceBuilder(self.organization).
                       with_location(far_location).
                       create())

        near_location = (LocationBuilder(self.organization).
                         with_long_lat(near_longitude, latitude).
                         create())
        near_service = (ServiceBuilder(self.organization).
                        with_location(near_location).
                        create())

        poor_match_score = 0.2
        good_match_score = 0.8

        self.set_service_similarity_score(topic_id, far_service.id, good_match_score)
        self.set_service_similarity_score(topic_id, near_service.id, poor_match_score)

        url = ('/v1/services_at_location/?related_to_topic={0}&user_location={1},{2}&proximity={1},{2}'.
               format(topic_id, user_longitude, latitude))

        json = self.client.get(url).json()

        self.assertEqual(len(json), 2)
        self.assertEqual(json[0]['service']['name'], near_service.name)
        self.assertEqual(json[1]['service']['name'], far_service.name)

    def test_orders_two_equally_good_match_by_distance(self):
        topic_id = 'the-topic-id'
        create_topics([topic_id])

        latitude = 0
        user_longitude = 0
        near_longitude = 0.0001
        far_longitude = 0.0002

        far_location = (LocationBuilder(self.organization).
                        with_long_lat(far_longitude, latitude).
                        create())
        far_service = (ServiceBuilder(self.organization).
                       with_location(far_location).
                       create())

        near_location = (LocationBuilder(self.organization).
                         with_long_lat(near_longitude, latitude).
                         create())
        near_service = (ServiceBuilder(self.organization).
                        with_location(near_location).
                        create())

        good_match_score = 0.8

        self.set_service_similarity_score(topic_id, far_service.id, good_match_score)
        self.set_service_similarity_score(topic_id, near_service.id, good_match_score)

        url = ('/v1/services_at_location/?related_to_topic={0}&user_location={1},{2}&proximity={1},{2}'.
               format(topic_id, user_longitude, latitude))

        json = self.client.get(url).json()

        self.assertEqual(len(json), 2)
        self.assertEqual(json[0]['service']['name'], near_service.name)
        self.assertEqual(json[1]['service']['name'], far_service.name)

    def test_can_full_text_search_on_service_name(self):
        service_at_locations = ServiceAtLocationBuilder().create_many()
        service_name = service_at_locations[0].service.name
        response = (self.client.get('/v1/services_at_location/?search={0}'.format(service_name)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['service']['name'], service_name)

    def test_can_full_text_search_on_service_description(self):
        service_at_locations = ServiceAtLocationBuilder().create_many()
        service_description = service_at_locations[0].service.description
        response = (self.client.get('/v1/services_at_location/?search={0}'.format(service_description)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['service']['description'], service_description)

    def test_can_full_text_search_on_location_name(self):
        service_at_locations = ServiceAtLocationBuilder().create_many()
        location_name = service_at_locations[0].location.name
        response = (self.client.get('/v1/services_at_location/?search={0}'.format(location_name)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location']['name'], location_name)

    def test_can_full_text_search_on_location_description(self):
        service_at_locations = ServiceAtLocationBuilder().create_many()
        location_description = service_at_locations[0].location.description
        response = (self.client.get('/v1/services_at_location/?search={0}'.format(location_description)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location']['description'], location_description)

    def test_can_filter_by_location_id(self):
        service_at_locations = ServiceAtLocationBuilder().create_many()
        expected_service_at_location = service_at_locations[0]
        location_id = expected_service_at_location.location.id
        response = (self.client.get('/v1/locations/{0}/services_at_location/'
                                    .format(location_id)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location']['name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service']['name'], expected_service_at_location.service.name)

    def test_can_filter_by_location_id_and_service_id(self):
        service_at_locations = ServiceAtLocationBuilder().create_many()
        expected_service_at_location = service_at_locations[0]
        location_id = expected_service_at_location.location.id
        service_id = expected_service_at_location.service.id
        response = (self.client.get('/v1/locations/{0}/services/{1}/services_at_location/'
                                    .format(location_id, service_id)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location']['name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service']['name'], expected_service_at_location.service.name)

    def test_can_filter_by_service_id(self):
        service_at_locations = ServiceAtLocationBuilder().create_many()
        expected_service_at_location = service_at_locations[0]
        service_id = expected_service_at_location.service.id
        response = (self.client.get('/v1/services/{0}/services_at_location/'
                                    .format(service_id)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location']['name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service']['name'], expected_service_at_location.service.name)

    def test_can_filter_by_service_id_and_location_id(self):
        service_at_locations = ServiceAtLocationBuilder().create_many()
        expected_service_at_location = service_at_locations[0]
        service_id = expected_service_at_location.service.id
        location_id = expected_service_at_location.location.id
        response = (self.client.get('/v1/services/{0}/locations/{1}/services_at_location/'
                                    .format(service_id, location_id)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location']['name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service']['name'], expected_service_at_location.service.name)

    def test_can_page(self):
        ServiceAtLocationBuilder().create_many(count=30)
        response = self.client.get('/v1/services_at_location/?per_page=10&page=2')
        json = response.json()
        self.assertEqual(len(json), 10)

    def test_can_filter_by_taxonomy(self):
        taxonomy_terms = TaxonomyTermBuilder().create_many()
        service = ServiceBuilder(self.organization).with_taxonomy_terms(taxonomy_terms).create()
        location = LocationBuilder(self.organization).create()
        expected_service_at_location = ServiceAtLocation.objects.create(service=service,
                                                                        location=location)
        response = (self.client.get('/v1/services_at_location/?taxonomy_terms={0}.{1}'
                                    .format(taxonomy_terms[0].taxonomy_id, taxonomy_terms[0].name)))
        json = response.json()
        self.assertEqual(len(json), 1)
        self.assertEqual(json[0]['location']['name'], expected_service_at_location.location.name)
        self.assertEqual(json[0]['service']['name'], expected_service_at_location.service.name)

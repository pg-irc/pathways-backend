import subprocess
import json
from human_services.locations.tests.helpers import LocationBuilder
from human_services.services_at_location.tests.helpers import (set_location_for_service,
                                                               set_service_similarity_score)
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from newcomers_guide.tests.helpers import create_topic
from common.testhelpers.random_test_values import a_string, a_latitude, a_longitude
from django.test.testcases import LiveServerTestCase

class ServicesAtLocationIntegrationTests(LiveServerTestCase):
    def test_get_service_from_server(self):
        organization = OrganizationBuilder().create()
        service = ServiceBuilder(organization).create()
        longitude = a_longitude()
        latitude = a_latitude()
        location = LocationBuilder(organization).with_long_lat(longitude, latitude).create()
        set_location_for_service(service.id, location.id)
        topic_id = a_string()
        create_topic(topic_id)
        set_service_similarity_score(topic_id, service.id, 0.9)
        host = self.live_server_url
        working_directory = '../pathways-frontend/'
        output = subprocess.run(args=[("yarn run ts-node src/api/integratinon_test.ts" +
                                       " --host " + host +
                                       " --topic " + topic_id +
                                       " --latitude " + str(latitude) +
                                       " --longitude " + str(longitude))],
                                cwd=working_directory,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                check=True)
        response = output.stdout.decode('utf-8')
        start_index = response.find('START_OF_RESPONSE') + len('START_OF_RESPONSE')
        end_index = response.find('END_OF_RESPONSE')
        response = response[start_index:end_index].strip()
        response = json.loads(response)
        self.assertEqual(response['results'][0]['service']['id'], service.id)

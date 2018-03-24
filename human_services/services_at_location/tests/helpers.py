from human_services.locations.models import ServiceAtLocation
from human_services.services.tests.helpers import ServiceBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.locations.tests.helpers import LocationBuilder


class ServiceAtLocationBuilder:
    def create_many(self, count=3):
        organization = OrganizationBuilder().create()
        return ([ServiceAtLocation.objects.create(
                 location=LocationBuilder(organization).create(),
                 service=ServiceBuilder(organization).create())
                 for _ in range(0, count)])

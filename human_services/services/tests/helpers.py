from human_services.services import models
from common.testhelpers.random_test_values import a_string

class ServiceBuilder:
    def __init__(self, organization):
        self.service_id = a_string()
        self.organization = organization
        self.name = a_string()
        self.description = a_string()
        self.taxonomy_terms = []

    def with_id(self, service_id):
        self.service_id = service_id
        return self

    def with_name(self, name):
        self.name = name
        return self

    def with_description(self, description):
        self.description = description
        return self

    def with_taxonomy_terms(self, taxonomy_terms):
        self.taxonomy_terms = taxonomy_terms
        return self

    def build(self):
        result = models.Service()
        result.id = self.service_id
        result.name = self.name
        result.organization = self.organization
        result.description = self.description
        for taxonomy_term in self.taxonomy_terms:
            result.taxonomy_terms.add(taxonomy_term)
        return result

    def create(self):
        result = self.build()
        result.save()
        return result

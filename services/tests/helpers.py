from services import models

class ServiceBuilder:
    def __init__(self, organization):
        self.id = 'the_default_id'
        self.organization = organization
        self.name = 'default name'
        self.description = 'default description'
        self.taxonomy_terms = []

    def with_id(self, id):
        self.id = id
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
        result.id = self.id
        result.name = self.name
        result.organization = self.organization
        result.description = self.description
        for taxonomy_term in self.taxonomy_terms:
            result.taxonomy_terms.add(taxonomy_term)
        return result

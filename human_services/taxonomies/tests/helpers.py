from human_services.taxonomies import models
from common.testhelpers.random_test_values import a_string

class TaxonomyTermBuilder:
    def __init__(self):
        self.taxonomy_id = a_string()
        self.name = a_string()

    def with_taxonomy_id(self, taxonomy_id):
        self.taxonomy_id = taxonomy_id
        return self

    def with_name(self, name):
        self.name = name
        return self

    def build(self):
        result = models.TaxonomyTerm()
        result.taxonomy_id = self.taxonomy_id
        result.name = self.name
        return result

    def create(self):
        result = self.build()
        result.save()
        return result

    def create_many(self, n=3):
        terms = []
        for _ in range(0, n):
            terms.append(TaxonomyTermBuilder().create())
        return terms

from services import models

class ServiceBuilder:
    def __init__(self, organization):
        self.id = 'the_default_id'
        self.organization = organization
        self.name = 'default name'
        self.description = 'default description'

    def with_id(self, id):
        self.id = id
        return self

    def with_name(self, name):
        self.name = name
        return self

    def with_description(self, description):
        self.description = description
        return self

    def build(self):
        result = models.Service()
        result.id = self.id
        result.name = self.name
        result.organization = self.organization
        result.description = self.description
        return result

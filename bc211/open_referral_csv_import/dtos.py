from .validate import required_string, optional_string


class Organization:
    def __init__(self, **kwargs):
        self.id = required_string('id', kwargs)
        self.name = required_string('name', kwargs)
        self.alternate_name = optional_string('alternate_name', kwargs)
        self.description = optional_string('description', kwargs)
        self.website = optional_string('website', kwargs)
        self.email = optional_string('email', kwargs)


class Service:
    def __init__(self, **kwargs):
        self.id = required_string('id', kwargs)
        self.organization_id = required_string('organization_id', kwargs)
        self.name = required_string('name', kwargs)
        self.alternate_name = optional_string('alternate_name', kwargs)
        self.description = optional_string('description', kwargs)
        self.email = optional_string('email', kwargs)
        self.website = optional_string('website', kwargs)
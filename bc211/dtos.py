from bc211 import validate

class Organization:
    def __init__(self, **kwargs):
        self.id = validate.required_string('id', kwargs)
        self.name = validate.required_string('name', kwargs)
        self.description = validate.optional_string('description', kwargs)
        self.website = validate.optional_string('website', kwargs)
        self.email = validate.optional_string('email', kwargs)
        self.locations = kwargs['locations']


class Location:
    def __init__(self, **kwargs):
        self.id = validate.required_string('id', kwargs)
        self.name = validate.required_string('name', kwargs)
        self.organization_id = validate.required_string('organization_id', kwargs)
        self.description = validate.optional_string('description', kwargs)
        self.spatial_location = validate.optional_object(SpatialLocation, 'spatial_location', kwargs)


class SpatialLocation:
    def __init__(self, **kwargs):
        self.latitude = validate.required_float('latitude', kwargs)
        self.longitude = validate.required_float('longitude', kwargs)

class Taxonomy:
    def __init__(self, vocabulary, name):
        self.vocabulary = slugify(vocabulary)
        self.name = slugify(name)

    def __hash__(self):
        return hash(self.vocabulary) ^ hash(self.name)

    def __eq__(self, other):
        return self.vocabulary == other.vocabulary and self.name == other.name

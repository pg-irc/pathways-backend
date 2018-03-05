from drf_yasg import openapi
from common.filters import ProximityFilter, TaxonomyFilter

class ManualParameters:
    @staticmethod
    def get_proximity_parameter():
        return (openapi.Parameter('proximity',
                                   openapi.IN_QUERY,
                                   description=ProximityFilter.filter_description,
                                   type=openapi.TYPE_STRING,
                                   # Regex representing a latitude and longitude.
                                   # Valid patterns consist of two integers or floats, comma separated, with
                                   # optional + or - prefixes. One space after the comma is allowed here.
                                   pattern=r'^[-+]?[0-9]+\.?[0-9]*,\s?[-+]?[0-9]+\.?[0-9]*$'))

    @staticmethod
    def get_taxonomy_terms_parameter():
        return (openapi.Parameter('taxonomy_terms',
                                   openapi.IN_QUERY,
                                   description=TaxonomyFilter.filter_description,
                                   type=openapi.TYPE_STRING,
                                   # One term followed by comma and additional terms zero or more times,
                                   # where a term consits of one or more letters/dashes, a dot, and more
                                   # letters/dashes. White space is allowed around the comma but not the
                                   # dots
                                   pattern=r'^[\w\-]+\.[\w\-]+(\W*,\W*[\w\-]+\.[\w\-]+)*$'))

from rest_framework.exceptions import ParseError

class ProximityParameterParser:
    errors = {
        'exactly_two_values': 'Exactly two comma separated values expected for proximity',
        'invalid_latitude_value_type': 'Latitude value provided to proximity must be able to represent a float',
        'invalid_longitude_value_type': 'Longitude value provided to proximity must be able to represent a float',
    }

    def __init__(self, parameter_value):
        self.parameter_value = parameter_value

    def build_valid_proximity_list(self):
        split_values = ([value.strip() for value
                         in self.parameter_value.split(',')])
        expected_length = 2
        if (len(split_values) != expected_length):
            raise (ParseError(self.errors['exactly_two_values']))
        return split_values

    def build_valid_latitude_value(self, value):
        try:
            valid_value = float(value)
        except ValueError:
            raise (ParseError(self.errors['invalid_latitude_value_type']))
        return valid_value

    def build_valid_longitude_value(self, value):
        try:
            valid_value = float(value)
        except ValueError:
            raise (ParseError(self.errors['invalid_longitude_value_type']))
        return valid_value

    def parse(self):
        if not self.parameter_value:
            return None
        proximity_list = self.build_valid_proximity_list()
        latitude = self.build_valid_latitude_value(proximity_list[0])
        longitude = self.build_valid_longitude_value(proximity_list[1])
        return [latitude, longitude]

    @classmethod
    def errors_to_string(cls):
        return ('{0}, {1}, {2}'.format(cls.errors['exactly_two_values'],
                                cls.errors['invalid_latitude_value_type'],
                                cls.errors['invalid_longitude_value_type']))


class TaxonomyParameterParser:
    errors = {
        'exactly_two_values': ('Exactly two period separated values expected for '
                               'each taxonomy id and term combination'),
        'empty_taxonomy_id': 'Taxonomy id cannot be empty',
        'empty_taxonomy_term': 'Taxonomy term cannot be empty',
    }

    def __init__(self, parameter_value):
        self.parameter_value = parameter_value

    def build_valid_taxonomy_pair(self, value):
        if len(value) != 2:
            raise (ParseError(self.errors['exactly_two_values']))
        taxonomy_id, term = value
        if not taxonomy_id:
            raise (ParseError(self.errors['empty_taxonomy_id']))
        if not term:
            raise (ParseError(self.errors['empty_taxonomy_term']))
        return (taxonomy_id, term)

    def parse(self):
        if not self.parameter_value:
            return None
        split_terms = [term.split('.') for term in self.parameter_value.split(',')]
        return [self.build_valid_taxonomy_pair(split_term) for split_term in split_terms]

    @classmethod
    def errors_to_string(cls):
        return ('{0}, {1}, {2}'.format(cls.errors['exactly_two_values'],
                                cls.errors['empty_taxonomy_id'],
                                cls.errors['empty_taxonomy_term']))

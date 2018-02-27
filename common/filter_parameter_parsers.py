from rest_framework.exceptions import ParseError

class ProximityParser:
    errors = {
        'exactly_two_values': 'Exactly two comma separated values expected for proximity',
        'invalid_value_types': 'Both values provided to proximity must be able to represent integers or floats'
    }

    @classmethod
    def parse_proximity(cls, value):
        if not value:
            return None
        proximity_as_list = ([value.strip() for value
                            in value.split(',')])
        proximity_as_list_expected_length = 2
        if (len(proximity_as_list) != proximity_as_list_expected_length):
            raise (ParseError(cls.errors['exactly_two_values']))
        try:
            latitude = float(proximity_as_list[0])
            longitude = float(proximity_as_list[1])
        except ValueError:
            raise (ParseError(cls.errors['invalid_value_types']))
        return [latitude, longitude]

    @classmethod
    def errors_to_string(cls):
        return ('{0}, {1}'.format(cls.errors['exactly_two_values'],
                 cls.errors['invalid_value_types']))

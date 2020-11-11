from .validate import required_string, optional_string, optional_object, required_float, required_country_code


class Address:
    def __init__(self, **kwargs):
        self.type = required_string('type', kwargs)
        self.location_id = required_string('location_id', kwargs)
        self.attention = optional_string('attention', kwargs)
        self.address = optional_string('address', kwargs)
        self.city = required_string('city', kwargs)
        self.state_province = optional_string('state_province', kwargs)
        self.postal_code = optional_string('postal_code', kwargs)
        self.country = required_country_code('country', kwargs)
        
        

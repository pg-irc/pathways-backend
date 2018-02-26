import string
import random
from . import private
from django.contrib.gis.geos import Point

private.set_random_seed_at_load_time()

def a_string(length=20, from_character_string=string.ascii_lowercase):
    return ''.join(random.choice(from_character_string) for x in range(length))

def a_website_address():
    return 'http://www.{0}.com'.format(a_string())

def an_email_address():
    return '{0}@{1}.com'.format(a_string(), a_string())

def an_integer(**kwargs):
    min_inclusive = kwargs.get('min', 0)
    max_inclusive = kwargs.get('max', 1000)

    return random.randint(min_inclusive, max_inclusive)

def a_float():
    return float(an_integer())

def a_point():
    srid = 4326
    return Point(a_float(), a_float(), srid=srid)

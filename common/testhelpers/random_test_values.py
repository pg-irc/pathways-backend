import string
import random
import common.testhelpers.details as details

details.set_random_seed_at_load_time()

def a_string(length=20, from_character_string=string.ascii_lowercase):
    return ''.join(random.choice(from_character_string) for x in range(length))

def a_website_address():
    return 'http://www.{0}.com'.format(a_string())

def an_email_address():
    return '{0}@{1}.com'.format(a_string(), a_string())

def an_integer():
    return random.randint(0, 1000)

def a_float():
    return float(an_integer())

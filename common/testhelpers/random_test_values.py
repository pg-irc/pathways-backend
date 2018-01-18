import string
import random
import common.testhelpers.details as details

details.set_random_seed_at_load_time()

def a_string():
    string_length = 20
    return ''.join(random.choice(string.ascii_lowercase) for x in range(string_length))

def a_website_address():
    return 'http://www.{0}.com'.format(a_string())

def an_email_address():
    return '{0}@{1}.com'.format(a_string(), a_string())

def an_integer():
    return random.randint(0, 1000)

def a_float():
    return float(an_integer())

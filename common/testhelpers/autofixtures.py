import string
import random
import common.testhelpers.details as details

details.set_random_seed_at_load_time()

def a_string():
    string_length = 32
    return ''.join(random.choice(string.ascii_letters) for x in range(string_length))

def a_number():
    return random.randint(0, 1000)

import random
import os

ENVIRONMENT_VARIABLE = 'RANDOM_SEED'

def set_random_seed_at_load_time():
    seed = get_seed_from_environment_variable()
    set_random_seed(seed)

def get_seed_from_environment_variable():
    default_seed = get_default_seed()
    return os.getenv(ENVIRONMENT_VARIABLE, default_seed)

def get_default_seed():
    max_seed_value = 100000000000
    seed_value = random.randint(0, max_seed_value)
    return str(seed_value)

def set_random_seed(seed):
    print('{0}={1}'.format(ENVIRONMENT_VARIABLE, seed))
    random.seed(seed)

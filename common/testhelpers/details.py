import random
import os

def set_random_seed_at_load_time():
    seed = get_seed_from_environment_variable()
    set_random_seed(seed)

def get_seed_from_environment_variable():
    return os.getenv('AUTOFIXTURE_SEED', get_default_seed())

def get_default_seed():
    max_seed_value = 100000000000
    return random.randint(0, max_seed_value)

def set_random_seed(seed):
    print('AUTOFIXTURE_SEED={0}'.format(seed))
    random.seed(seed)

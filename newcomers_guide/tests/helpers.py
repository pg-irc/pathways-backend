from search.models import Task
from common.testhelpers.random_test_values import a_string


def create_topic(the_id):
    Task(id=the_id, name=a_string(), description=a_string()).save()

from search.models import Task
from common.testhelpers.random_test_values import a_string, an_integer


def create_topic(the_id):
    Task(id=the_id, name=a_string(), description=a_string()).save()


class TopicBuilder():
    def __init__(self):
        self.id = an_integer()
        self.name = a_string()
        self.description = a_string()

    def build(self):
        result = Task()
        result.id = self.id
        result.name = self.name
        result.description = self.description
        return result

    def create(self):
        result = self.build()
        result.save()
        return result

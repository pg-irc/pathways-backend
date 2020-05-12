from content import models
from common.testhelpers.random_test_values import a_string

class AlertBuilder:
    def __init__(self):
        self.alert_id = a_string()
        self.title = a_string()
        self.description = a_string()

    def with_id(self, alert_id):
        self.alert_id = alert_id
        return self

    def with_title(self, title):
        self.title = title
        return self

    def with_description(self, description):
        self.description = description
        return self

    def build(self):
        result = models.Alert()
        result.id = self.alert_id
        result.title = self.title
        result.description = self.description
        return result

    def create(self):
        result = self.build()
        result.save()
        return result

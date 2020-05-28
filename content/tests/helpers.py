from content import models
from common.testhelpers.random_test_values import a_string


class AlertBuilder:
    def __init__(self):
        self.alert_id = a_string()
        self.heading = a_string()
        self.content = a_string()

    def with_id(self, alert_id):
        self.alert_id = alert_id
        return self

    def with_heading(self, heading):
        self.heading = heading
        return self

    def with_content(self, content):
        self.content = content
        return self

    def build(self):
        result = models.Alert()
        result.id = self.alert_id
        result.heading = self.heading
        result.content = self.content
        return result

    def create(self):
        result = self.build()
        result.save()
        return result

from common.testhelpers.random_test_values import a_string

class OpenReferralCsvOrganizationBuilder:
    def __init__(self):
        self.data = self.a_row()

    def a_row(self):
        organization_id = a_string()
        name = a_string()
        return [organization_id, name]
    
    def with_id(self, organization_id):
        self.data[0] = organization_id
        return self

    def with_name(self, name):
        self.data[1] = name
        return self
        
    def build(self):
        return self.data
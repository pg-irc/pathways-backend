from common.testhelpers.random_test_values import a_string

class OpenReferralCsvOrganizationBuilder:
    def __init__(self):
        self.data = self.a_row()

    def a_row(self):
        organization_id = a_string()
        name = a_string()
        alternate_name = ''
        description = ''
        email = ''
        return [organization_id, name, alternate_name, description, email]
    
    def with_id(self, organization_id):
        self.data[0] = organization_id
        return self

    def with_name(self, name):
        self.data[1] = name
        return self

    def with_alternate_name(self, alternate_name):
        self.data[2] = alternate_name
        return self
    
    def with_description(self, description):
        self.data[3] = description
        return self

    def with_email(self, email):
        self.data[4] = email
        return self
        
    def build(self):
        return self.data
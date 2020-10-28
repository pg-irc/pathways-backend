from common.testhelpers.random_test_values import a_string, an_email_address, a_website_address, a_latitude_as_a_string

class OpenReferralCsvOrganizationBuilder:
    def __init__(self):
        self.data = self.a_row()

    def a_row(self):
        organization_id = a_string()
        name = a_string()
        alternate_name = a_string()
        description = a_string()
        email = an_email_address()
        url = a_website_address()
        not_used_tax_status = a_string()
        not_used_tax_id = a_string()
        not_used_year_incorporated = a_string()
        not_used_legal_status = a_string()
        return [organization_id, name, alternate_name, description, email, url,
                not_used_tax_status, not_used_tax_id, not_used_year_incorporated, not_used_legal_status]
    
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

    def with_url(self, url):
        self.data[5] = url
        return self
        
    def build(self):
        return self.data


class OpenReferralCsvServiceBuilder:
    def __init__(self, organization):
        self.data = self.a_row(organization)

    def a_row(self, organization):
        service_id = a_string()
        organization_id = organization.id
        not_used_program_id = a_string()
        name = a_string()
        alternate_name = a_string()
        description = a_string()
        url = a_website_address()
        email = an_email_address()
        not_used_status = a_string()
        not_used_intepretation_services = a_string()
        not_used_application_process = a_string()
        not_used_wait_time = a_string()
        not_used_fees = a_string()
        not_used_accreditations = a_string()
        not_used_licenses = a_string()
        not_used_taxonomy_ids = a_string()

        return [service_id, organization_id, not_used_program_id, name, alternate_name, description, url, email,
                not_used_status, not_used_intepretation_services, not_used_application_process, not_used_wait_time,
                not_used_fees, not_used_accreditations, not_used_licenses, not_used_taxonomy_ids]
    
    def with_id(self, service_id):
        self.data[0] = service_id
        return self

    def with_organization_id(self, organization_id):
        self.data[1] = organization_id
        return self

    def with_name(self, name):
        self.data[3] = name
        return self
    
    def with_alternate_name(self, alternate_name):
        self.data[4] = alternate_name
        return self
    
    def with_description(self, description):
        self.data[5] = description
        return self

    def with_url(self, url):
        self.data[6] = url
        return self

    def with_email(self, email):
        self.data[7] = email
        return self
    
    def build(self):
        return self.data


class OpenReferralCsvLocationBuilder:
    def __init__(self, organization):
        self.data = self.a_row(organization)

    def a_row(self, organization):
        location_id = a_string()
        organization_id = organization.id
        name = a_string()
        alternate_name = a_string()
        description = a_string()
        not_used_transportation = a_string()
        latitude = a_latitude_as_a_string()
        return [location_id, organization_id, name, alternate_name, description, not_used_transportation, latitude]
    
    def with_id(self, location_id):
        self.data[0] = location_id
        return self

    def with_organization_id(self, organization_id):
        self.data[1] = organization_id
        return self
    
    def with_name(self, name):
        self.data[2] = name
        return self

    def with_alternate_name(self, alternate_name):
        self.data[3] = alternate_name
        return self
    
    def with_description(self, description):
        self.data[4] = description
        return self
    
    def with_latitude(self, latitude):
        self.data[6] = latitude
        return self

    def build(self):
        return self.data 
from common.testhelpers.random_test_values import (a_string, an_email_address, a_website_address,
                                                a_latitude_as_a_string, a_longitude_as_a_string)
from bc211.open_referral_csv_import import dtos


class OpenReferralCsvOrganizationBuilder:
    def __init__(self):
        self.organization_id = a_string()
        self.name = a_string()
        self.alternate_name = a_string()
        self.description = a_string()
        self.email = an_email_address()
        self.url = a_website_address()
    
    def with_id(self, organization_id):
        self.organization_id = organization_id
        return self

    def with_name(self, name):
        self.name = name
        return self

    def with_alternate_name(self, alternate_name):
        self.alternate_name = alternate_name
        return self
    
    def with_description(self, description):
        self.description = description
        return self

    def with_email(self, email):
        self.email = email
        return self

    def with_url(self, url):
        self.url = url
        return self
        
    def build(self):
        not_used_tax_status = a_string()
        not_used_tax_id = a_string()
        not_used_year_incorporated = a_string()
        not_used_legal_status = a_string()
        return [self.organization_id, self.name, self.alternate_name, self.description, self.email, self.url,
                not_used_tax_status, not_used_tax_id, not_used_year_incorporated, not_used_legal_status]

    def build_dto(self):
        return dtos.Organization(id=self.organization_id,
                                name=self.name,
                                alternate_name=self.alternate_name,
                                description=self.description,
                                email=self.email,
                                website=self.url)


class OpenReferralCsvServiceBuilder:
    def __init__(self, organization):
        self.service_id = a_string()
        self.organization_id = organization.id
        self.name = a_string()
        self.alternate_name = a_string()
        self.description = a_string()
        self.url = a_website_address()
        self.email = an_email_address()
    
    def with_id(self, service_id):
        self.service_id = service_id
        return self

    def with_organization_id(self, organization_id):
        self.organization_id = organization_id
        return self

    def with_name(self, name):
        self.name = name
        return self
    
    def with_alternate_name(self, alternate_name):
        self.alternate_name = alternate_name
        return self
    
    def with_description(self, description):
        self.description = description
        return self

    def with_url(self, url):
        self.url = url
        return self

    def with_email(self, email):
        self.email = email
        return self
    
    def build(self):
        not_used_program_id = a_string()
        not_used_status = a_string()
        not_used_intepretation_services = a_string()
        not_used_application_process = a_string()
        not_used_wait_time = a_string()
        not_used_fees = a_string()
        not_used_accreditations = a_string()
        not_used_licenses = a_string()
        not_used_taxonomy_ids = a_string()
        return [self.service_id, self.organization_id, not_used_program_id, self.name, self.alternate_name, self.description, self.url, self.email,
                not_used_status, not_used_intepretation_services, not_used_application_process, not_used_wait_time,
                not_used_fees, not_used_accreditations, not_used_licenses, not_used_taxonomy_ids]
    
    def build_dto(self):
        return dtos.Service(id=self.service_id,
                            organization_id=self.organization_id,
                            name=self.name,
                            alternate_name=self.alternate_name,
                            description=self.description,
                            website=self.url,
                            email=self.email)


class OpenReferralCsvLocationBuilder:
    def __init__(self, organization):
        self.location_id = a_string()
        self.organization_id = organization.id
        self.name = a_string()
        self.alternate_name = a_string()
        self.description = a_string()
        self.latitude = a_latitude_as_a_string()
        self.longitude = a_longitude_as_a_string()
    
    def with_id(self, location_id):
        self.location_id = location_id
        return self

    def with_organization_id(self, organization_id):
        self.organization_id = organization_id
        return self
    
    def with_name(self, name):
        self.name = name
        return self

    def with_alternate_name(self, alternate_name):
        self.alternate_name = alternate_name
        return self
    
    def with_description(self, description):
        self.description = description
        return self
    
    def with_latitude(self, latitude):
        self.latitude = latitude
        return self
    
    def with_longitude(self, longitude):
        self.longitude = longitude
        return self

    def build(self):
        not_used_transportation = a_string()
        return [self.location_id, self.organization_id, self.name, self.alternate_name, self.description, not_used_transportation, self.latitude, self.longitude]
    
    def build_dto(self):
        return dtos.Location(id=self.location_id,
                            organization_id=self.organization_id,
                            name=self.name,
                            alternate_name=self.alternate_name,
                            description=self.description,
                            spatial_location=dtos.SpatialLocation(latitude=self.latitude, longitude=self.longitude))


class OpenReferralCsvServiceAtLocationBuilder:
    def __init__(self, service, location):
        self.service_id = service.id
        self.location_id = location.id
    
    def with_service_id(self, service_id):
        self.service_id = service_id
        return self
    
    def with_location_id(self, location_id):
        self.location_id = location_id
        return self
    
    def build(self):
        not_used_id = a_string()
        not_used_description = a_string()
        return [not_used_id, self.service_id, self.location_id, not_used_description]
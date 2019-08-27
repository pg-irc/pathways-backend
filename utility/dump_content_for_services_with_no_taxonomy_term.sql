-- run this script with the follow command
-- psql -d pathways_local -F $',' -A -f utility/dump_content_for_services_with_no_taxonomy_term.sql > content.csv

select distinct
	service.id as service_id,
    serviceStrings.name as service_name,
    organizationStrings.name as organization_name,
    address.address
from
	services_service as service
    left outer join services_service_taxonomy_terms
        on(service.id = services_service_taxonomy_terms.service_id),
	services_service_translation as serviceStrings,
    organizations_organization as organization,
	organizations_organization_translation as organizationStrings,
	locations_location as location,
	locations_serviceatlocation as servicesAtLocation,
	locations_locationaddress as locationAddress,
	addresses_address as address
where
    service.id = serviceStrings.master_id and
    services_service_taxonomy_terms.service_id is null and 
    organization.id=organizationStrings.master_id and
	organization.id=service.organization_id and
	service.id=servicesAtLocation.service_id and
	location.id=servicesAtLocation.location_id and
	servicesAtLocation.location_id=locationAddress.location_id and
	locationAddress.address_id=address.id;
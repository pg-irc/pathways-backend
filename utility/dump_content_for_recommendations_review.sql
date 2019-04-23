-- psql -d pathways_local -F $'\t' -A -f utility/dump_content_for_recommendations_review.sql > content.csv

select distinct
	'"' || organizationStrings.name || '"' as organization_name, 
	organization.website as organization_website,
	organization.email as organization_email,
	service.id as service_id, 
	'"' || serviceStrings.name || '"' as service_name, 
	regexp_replace(serviceStrings.description, E'[\\n\\r\\t;,]+', ' ', 'g' ) as service_description,
	regexp_replace(address.address, E'[\\n\\r;,]+', ' ', 'g' ) as street_address, 
	'"' || address.city || '"' as city, 
	'"' || address.postal_code || '"' as postal_code,
	ST_X(location.point) as longitude,
	ST_Y(location.point) as latitude
from
	services_service as service, 
	services_service_translation as serviceStrings, 
	organizations_organization as organization, 
	organizations_organization_translation as organizationStrings, 
	locations_location as location,
	locations_serviceatlocation as servicesAtLocation, 
	locations_locationaddress as locationAddress, 
	addresses_address as address 
where
	service.id=serviceStrings.master_id and 
	organization.id=organizationStrings.master_id and 
	organization.id=service.organization_id and 
	service.id=servicesAtLocation.service_id and 
	location.id=servicesAtLocation.location_id and
	servicesAtLocation.location_id=locationAddress.location_id and 
	locationAddress.address_id=address.id and 
	locationAddress.address_type_id='physical_address' 
order by
	organization_name, service_name;

-- use csvtojson (https://github.com/Keyang/node-csvtojson/), not csv2json

-- sudo npm install --global csvtojson

-- psql -d pathways_local -F $',' -A -f utility/dump_content_for_algolia.sql | head -n -1 | csvtojson --colParser='{"_geoloc.lng":"number","_geoloc.lat":"number"}' > content.json

-- Column names _geoloc.lng and _geoloc.lat are special. csvtojson understands to convert this to 
-- "_geoloc":{"lng":-122.724,"lat":49.110044}. The --colParser option define the lat and long to be 
-- numbers, rather than strings. With the special names _geoloc, lng and lat, Algolia understands 
-- this to mean a geolocation point.

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
	ST_X(location.point) as "_geoloc.lng",
	ST_Y(location.point) as "_geoloc.lat"
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

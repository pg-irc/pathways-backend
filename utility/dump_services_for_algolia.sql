-- use csvtojson (https://github.com/Keyang/node-csvtojson/), not csv2json

-- sudo npm install --global csvtojson

-- psql -d pathways_local -F $',' -A -f utility/dump_services_for_algolia.sql | head -n -1 | csvtojson --colParser='{"_geoloc.lng":"number","_geoloc.lat":"number","organization.service_count":"number"}' > services.json

-- Column names _geoloc.lng and _geoloc.lat are special. csvtojson understands to convert this to 
-- "_geoloc":{"lng":-122.724,"lat":49.110044}. The --colParser option define the lat and long to be 
-- numbers, rather than strings. With the special names _geoloc, lng and lat, Algolia understands 
-- this to mean a geolocation point.

-- TODO, add:
-- phone numbers with type

select distinct
	service.id as service_id,
	'"' || serviceStrings.name || '"' as service_name,
	left(regexp_replace(serviceStrings.description, E'[\\n\\r\\t;,]+', ' ', 'g' ), 5000) as service_description,
	organization.id as "organization.id",
	'"' || organizationStrings.name || '"' as "organization.name",
	organization.website as "organization.website",
	organization.email as "organization.email",
	counts.service_count as "organization.service_count",
	regexp_replace(address.address, E'[\\n\\r;,]+', ' ', 'g' ) as "address.address",
	'"' || address.city || '"' as "address.city",
	'"' || address.state_province || '"' as "address.state_province",
	'"' || address.postal_code || '"' as "address.postal_code",
	address.country as "address.country",
	ST_X(location.point) as "_geoloc.lng",
	ST_Y(location.point) as "_geoloc.lat"
from
	services_service as service,
	services_service_translation as serviceStrings,
	locations_location as location,
	locations_serviceatlocation as servicesAtLocation,
	locations_locationaddress as locationAddress,
	addresses_address as address,
	organizations_organization as organization,
	organizations_organization_translation as organizationStrings,
	(select
		count(s.id) as service_count,
		o.id as organization_id
	from
		services_service as s,
		organizations_organization as o
	where
		s.organization_id=o.id
	group by
		o.id
	) as counts
where
	service.id=serviceStrings.master_id and
	service.id=servicesAtLocation.service_id and
	location.id=servicesAtLocation.location_id and
	servicesAtLocation.location_id=locationAddress.location_id and
	locationAddress.address_id=address.id and
	locationAddress.address_type_id='physical_address' and
	organization.id=service.organization_id and
	organization.id=organizationStrings.master_id and
	organization.id=counts.organization_id
order by
	service_name;

-- psql -d pathways_local -F $'\t' -A -f utility/dump_content_for_recommendations_review.sql > content.csv

select distinct
	s.id as service_id, 
	'"' || ot.name || '"' as organization_name, 
	'"' || st.name || '"' as service_name, 
	regexp_replace(a.address, E'[\\n\\r;,]+', ' ', 'g' ) as street_address, 
	'"' || a.city || '"' as city, 
	'"' || a.postal_code || '"' as postal_code, 
	regexp_replace(st.description, E'[\\n\\r\\t;,]+', ' ', 'g' ) as description 
from 
	services_service as s, 
	services_service_translation as st, 
	organizations_organization as o, 
	organizations_organization_translation as ot, 
	locations_serviceatlocation as sl, 
	locations_locationaddress as la, 
	addresses_address as a 
where 
	s.id=st.master_id and 
	o.id=ot.master_id and 
	o.id=s.organization_id and 
	s.id=sl.service_id and 
	sl.location_id=la.location_id and 
	la.address_id=a.id and 
	la.address_type_id='physical_address' 
order by organization_name;

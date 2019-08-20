-- psql -d pathways_local -F $',' -A -f utility/dump_content_for_services_without_taxonomy.sql > content.csv

-- For use in situations when we need to find :

select distinct 
    services_service_translation.master_id, services_service_translation.name
from 
    services_service_translation 
left outer join services_service_taxonomy_terms
    on (services_service_translation.master_id = services_service_taxonomy_terms.service_id)
where 
    services_service_taxonomy_terms.service_id is null
order by 
    services_service_translation.name;

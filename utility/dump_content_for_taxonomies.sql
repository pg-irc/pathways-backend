-- psql -d pathways_local -F $',' -A -f utility/dump_content_for_recommendations_review.sql \ 
-- -v taxonomy_id='bc211-why' > content.csv

-- For use in situations when we need the taxonomies and their frequency:

select distinct 
    taxonomies_taxonomyterm.name, count(taxonomies_taxonomyterm.name)
from 
    services_service_translation 
left outer join services_service_taxonomy_terms
    on (services_service_translation.master_id = services_service_taxonomy_terms.service_id)
inner join taxonomies_taxonomyterm
    on (services_service_taxonomy_terms.taxonomyterm_id = taxonomies_taxonomyterm.id)
where 
    taxonomies_taxonomyterm.taxonomy_id = :taxonomy_id
group by 
    taxonomies_taxonomyterm.name;

--psql -d pathways_local -F $',' -A -f utility/dump_content_for_taxonomies.sql  > content.csv
-- For use in situations when we need the task taxonomies and their frequency:

select topic_taxonomy_terms.task_id, taxonomies_taxonomyterm.taxonomy_id, taxonomies_taxonomyterm.name
from
    topic_taxonomy_terms,
    taxonomies_taxonomyterm
where
    topic_taxonomy_terms.taxonomyterm_id = taxonomies_taxonomyterm.id;
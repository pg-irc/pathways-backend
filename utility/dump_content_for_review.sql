-- To execute:
-- psql -d database -f this_file > output.csv
-- e.g.
-- psql -d pathways_local -f utility/dump_content_for_review.sql > content_for_review.csv

copy (
	select topic.master_id as topic_id, 
		topic.name as topic_title, 
		concat(taxonomy_terms.taxonomy_id, ':', taxonomy_terms.name) as taxonomy_term, 
		topic.description as topic_content 
	from search_task_translation as topic, 
		topic_taxonomy_terms, 
		taxonomies_taxonomyterm as taxonomy_terms 
	where topic.master_id = topic_taxonomy_terms.task_id and 
		topic_taxonomy_terms.taxonomyterm_id = taxonomy_terms.id 
	order by topic.master_id
) to stdout with csv header

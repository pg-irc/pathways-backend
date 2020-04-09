psql -d pathways_local -F $',' -A -t -c \
    'select location_id, phone_number, phone_number_type_id from phone_at_location_phoneatlocation' > phones_data.csv

psql -d pathways_local -F $',' -A -t -c \
    "select s.service_id, t.name from services_service_taxonomy_terms as s, taxonomies_taxonomyterm as t where s.taxonomyterm_id=t.id and t.taxonomy_id like 'bc211-%' " > taxonomy_data.csv

psql -d pathways_local -F $',' -A -f utility/algolia/dump_services.sql |\
    tail -r | tail -n +2 | tail -r |\
    csvtojson --colParser='{"_geoloc.lng":"number","_geoloc.lat":"number","organization.service_count":"number"}' > services.json

python utility/algolia/add_phone_numbers_to_services.py phones_data.csv taxonomy_data.csv services.json output_data.json

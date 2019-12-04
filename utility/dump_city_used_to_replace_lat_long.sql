-- To execute:
-- psql -d database -f this_file > output.csv
-- e.g.
-- psql -d pathways_local -f utility/dump_city_used_to_replace_lat_long.sql > city.csv
-- use http://geocoder.ca/textscan to get the corresponding latlong for these cities

select distinct 
    city
from 
    locations_location, locations_locationaddress, addresses_address
where 
    locations_locationaddress.location_id = locations_location.id and 
    locations_locationaddress.address_id = addresses_address.id and
    locations_location.point is NULL

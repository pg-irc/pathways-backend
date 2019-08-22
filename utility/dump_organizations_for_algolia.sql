-- use csvtojson (https://github.com/Keyang/node-csvtojson/), not csv2json

-- sudo npm install --global csvtojson

-- psql -d pathways_local -F $',' -A -f utility/dump_organizations_for_algolia.sql | head -n -1 | csvtojson > organizations.json

select distinct
	'"' || organizationStrings.name || '"' as organization_name,
	regexp_replace(organizationStrings.description, E'[\\n\\r\\t;,]+', ' ', 'g' ) as organization_description,
	organization.website as organization_website,
	organization.email as organization_email
from
	organizations_organization as organization,
	organizations_organization_translation as organizationStrings
where
	organization.id=organizationStrings.master_id
order by
	organization_name;

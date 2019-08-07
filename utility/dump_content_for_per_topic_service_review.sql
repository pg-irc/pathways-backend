-- Pass topic ids on the command line as a list using -v, mind the single and double quotes!

-- command for getting the recommended services for all the topics in Things to do right away

-- psql -d pathways_local -F $'\t' -A -f utility/dump_content_for_per_topic_service_review.sql \
-- -v task_ids="('contact-workers-at-your-local-settlement-agency',\
-- 'give-your-canadian-address-to-immigration-refugees-and-citizenship-canada',\
-- 'finding-a-place-to-rent',\
-- 'know-your-rights-as-a-tenant',\
-- 'apply-for-the-canada-child-benefit-for-children-under-18-years-old',\
-- 'opening-a-bank-account',\
-- 'get-your-bc-services-card',\
-- 'register-for-the-medical-services-plan-msp',\
-- 'the-interim-federal-health-program-refugees-and-refugee-claimants',\
-- 'register-for-english-classes',\
-- 'registering-your-child-in-a-public-school',\
-- 'applying-for-a-driver_s-licence',\
-- 'apply-for-a-social-insurance-number-sin')"> content.csv

select distinct
	taskSimilarity.task_id as topic_id,
	to_char(taskSimilarity.similarity_score, '9.99') as score,
	service.id as service_id,
	'' as "exclude?",
	'"' || organizationStrings.name || '"' as organization_name,
	'"' || serviceStrings.name || '"' as service_name,
	regexp_replace(serviceStrings.description, E'[\\n\\r\\t;,]+', ' ', 'g' ) as service_description,
	'"' || address.city || '"' as city
	-- organization.website as organization_website,
	-- organization.email as organization_email,
	-- regexp_replace(address.address, E'[\\n\\r;,]+', ' ', 'g' ) as street_address,
	-- '"' || address.postal_code || '"' as postal_code,
	-- ST_X(location.point) as longitude,
	-- ST_Y(location.point) as latitude
from
	search_taskservicesimilarityscore as taskSimilarity,
	services_service as service,
	services_service_translation as serviceStrings,
	organizations_organization as organization,
	organizations_organization_translation as organizationStrings,
	locations_location as location,
	locations_serviceatlocation as servicesAtLocation,
	locations_locationaddress as locationAddress,
	addresses_address as address
where
	taskSimilarity.task_id in :task_ids and
	taskSimilarity.service_id=service.id and
	service.id=serviceStrings.master_id and
	organization.id=organizationStrings.master_id and
	organization.id=service.organization_id and
	service.id=servicesAtLocation.service_id and
	location.id=servicesAtLocation.location_id and
	servicesAtLocation.location_id=locationAddress.location_id and
	locationAddress.address_id=address.id and
	locationAddress.address_type_id='physical_address'
order by
	topic_id, organization_name, service_name;

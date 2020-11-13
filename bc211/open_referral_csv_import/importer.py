import logging
from bc211.open_referral_csv_import.organization import import_organizations_file
from bc211.open_referral_csv_import.service import import_services_file
from bc211.open_referral_csv_import.location import import_locations_file
from bc211.open_referral_csv_import.services_at_location import import_services_at_location_file
from bc211.open_referral_csv_import.address import import_addresses_file
from bc211.open_referral_csv_import.phone import import_phones_file
from bc211.open_referral_csv_import.taxonomy import import_taxonomy_file
from bc211.open_referral_csv_import.service_taxonomy import import_services_taxonomy_file

LOGGER = logging.getLogger(__name__)

# TODO add spatial location to locations where missing when addresses file is imported

def import_open_referral_files(root_folder):
    try:
        import_organizations_file(root_folder)
        import_services_file(root_folder)
        import_locations_file(root_folder)
        import_services_at_location_file(root_folder)
        import_addresses_file(root_folder)
        import_phones_file(root_folder)
        import_taxonomy_file(root_folder)
        import_services_taxonomy_file(root_folder)
    except Exception as error:
        LOGGER.error(error)
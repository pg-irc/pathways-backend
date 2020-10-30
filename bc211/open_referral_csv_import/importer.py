import logging
from .organization import import_organizations_file
from .service import import_services_file
from .location import import_locations_file
from .services_at_location import import_services_at_location_file
from .address import import_addresses_file

LOGGER = logging.getLogger(__name__)

# TODO add spatial location to locations where missing when addresses file is imported

def import_open_referral_files(root_folder):
    try:
        import_organizations_file(root_folder)
        import_services_file(root_folder)
        import_locations_file(root_folder)
        import_services_at_location_file(root_folder)
        import_addresses_file(root_folder)
    except Exception as error:
        LOGGER.error(error)
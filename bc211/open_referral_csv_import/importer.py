import logging
from .organization import import_organizations_file


LOGGER = logging.getLogger(__name__)


def import_open_referral_files(root_folder):
    try:
        import_organizations_file(root_folder)
    except Exception as error:
        LOGGER.error(error)
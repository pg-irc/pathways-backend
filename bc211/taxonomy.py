import logging
from taxonomies.models import TaxonomyTerm

LOGGER = logging.getLogger(__name__)


def save_service_taxonomy_terms(taxonomy_terms, service_active_record, counters):
    for taxonomy_term in taxonomy_terms:
        taxonomy_term_active_record = create_taxonomy_term_active_record(
            taxonomy_term,
            counters
        )
        service_active_record.taxonomy_terms.add(taxonomy_term_active_record)
        LOGGER.debug('Imported service taxonomy term')
    service_active_record.save()


def create_taxonomy_term_active_record(record, counters):
    taxonomy_term_active_record, created = TaxonomyTerm.objects.get_or_create(
        taxonomy_id=record.taxonomy_id,
        name=record.name
    )
    if created:
        counters.count_taxonomy_term()
        LOGGER.debug('Taxonomy term "%s" "%s"', record.taxonomy_id, record.name)
    return taxonomy_term_active_record

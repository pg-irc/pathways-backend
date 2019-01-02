from django.utils import translation
from search.models import Task
from taxonomies.models import TaxonomyTerm


def save_tasks(tasks):
    Task.objects.all().delete()
    translation.activate('en')
    for _, task in tasks['taskMap'].items():
        record = Task()
        record.id = task['id']
        record.name = task['title']['en']
        record.description = task['description']['en']

        for taxonomy_term in task['taxonomyTerms']:
            taxonomy_term_record = get_or_create_taxonomy_term(taxonomy_term)
            record.taxonomy_terms.add(taxonomy_term_record)

        record.save()


def get_or_create_taxonomy_term(taxonomy_term):
    taxonomy_id = taxonomy_term['taxonomyId']
    name = taxonomy_term['taxonomyTermId']
    taxonomy_term_record, _ = TaxonomyTerm.objects.get_or_create(
        taxonomy_id=taxonomy_id,
        name=name
    )
    return taxonomy_term_record

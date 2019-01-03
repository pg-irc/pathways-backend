import collections
from django.utils import translation
from search.models import Task
from bc211.importer import create_taxonomy_term_active_record


def save_topics(tasks, counts):
    Task.objects.all().delete()
    translation.activate('en')
    for _, task in tasks['taskMap'].items():
        record = Task()
        record.id = task['id']
        record.name = task['title']['en']
        record.description = task['description']['en']
        record.save()

        for taxonomy_term in task['taxonomyTerms']:
            taxonomy_term_record = get_or_create_taxonomy_term(taxonomy_term, counts)
            record.taxonomy_terms.add(taxonomy_term_record)

        record.save()


def get_or_create_taxonomy_term(taxonomy_term, counts):
    taxonomy_term_type = collections.namedtuple('taxonomy_term_type',
                                                ['taxonomy_id', 'name'])
    taxonomy_term = taxonomy_term_type(taxonomy_id=taxonomy_term['taxonomyId'],
                                       name=taxonomy_term['taxonomyTermId'])
    return create_taxonomy_term_active_record(taxonomy_term, counts)

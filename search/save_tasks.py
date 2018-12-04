from django.utils import translation
from search.models import Task


def save_tasks(tasks):
    Task.objects.all().delete()
    translation.activate('en')
    for _, task in tasks['taskMap'].items():
        record = Task()
        record.id = task['id']
        record.name = task['title']['en']
        record.description = task['description']['en']
        record.save()

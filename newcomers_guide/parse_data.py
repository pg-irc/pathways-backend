import os
import json
import collections
from django.core import exceptions
from newcomers_guide.clean_data import clean_text


class TaxonomyTermReference:
    def __init__(self, taxonomy_id, taxonomy_term_id, content_type, content_id):
        self.taxonomy_id = taxonomy_id
        self.taxonomy_term_id = taxonomy_term_id
        self.content_type = content_type
        self.content_id = content_id


class TaskBuilder:
    def __init__(self):
        self.task = {}

    def get_id(self):
        return self.task['id']

    def set_id(self, the_id):
        self.task['id'] = the_id
        return self

    def set_title_in_locale(self, locale, title):
        self.ensure_key_exist('title')
        self.task['title'][locale] = title
        return self

    def set_description_in_locale(self, locale, description):
        self.ensure_key_exist('description')
        self.task['description'][locale] = description
        return self

    def ensure_key_exist(self, key):
        if key not in self.task:
            self.task[key] = {}

    def to_task(self):
        return self.task

    def to_json(self):
        return json.dumps(self.task)


def parse_file_path(path):
    parsed_file_path = collections.namedtuple('parsed_file_path',
                                              ['chapter', 'type', 'id', 'locale', 'title'])
    split_path = path.split(os.sep)
    length = len(split_path)
    if length < 5:
        raise Exception(path + ': path is too short')
    name = split_path[length-1]
    split_name = name.split('.')
    return parsed_file_path(chapter=split_path[length - 4],
                            type=split_path[length - 3],
                            id=split_path[length - 2],
                            title=split_name[1],
                            locale=split_name[0])


def parse_task_files(file_specs):
    builders = {}
    for spec in file_specs:
        path = spec[0]
        description = clean_text(spec[1])

        parsed_path = parse_file_path(path)
        task_id = parsed_path.id

        if parsed_path.type == 'tasks':
            ensure_builder_exists_for_task(builders, task_id)
            add_properties_for_locale(builders[task_id], parsed_path, description)

    return make_task_map(builders)


def ensure_builder_exists_for_task(builders, task_id):
    if task_id not in builders:
        builders[task_id] = TaskBuilder()
        builders[task_id].set_id(task_id)


def add_properties_for_locale(builder, parsed_path, description):
    locale = parsed_path.locale
    builder.set_title_in_locale(locale, parsed_path.title)
    builder.set_description_in_locale(locale, description)


def make_task_map(builders):
    tasks = {}
    for key in builders:
        tasks[key] = builders[key].to_task()
    return tasks


def parse_taxonomy_files(file_specs):
    result = []
    for spec in file_specs:
        path = spec[0]
        file_content = spec[1]
        parsed_path = parse_file_path(path)
        content_id = parsed_path.id
        content_type = parsed_path.type
        parsed_terms = parse_taxonomy_terms(file_content)
        for term in parsed_terms:
            result.append(TaxonomyTermReference(taxonomy_id=term.taxonomy_id,
                                                taxonomy_term_id=term.taxonomy_term_id,
                                                content_type=content_type,
                                                content_id=content_id))
    return result


def parse_taxonomy_terms(taxonomy_terms):
    taxonomy_term_type = collections.namedtuple('taxonomy_term_type',
                                                ['taxonomy_id', 'taxonomy_term_id'])
    result = []
    items = taxonomy_terms.split(',')
    for item in items:
        validate_taxonomy_item(item)
        split_item = item.split(':')
        result.append(taxonomy_term_type(taxonomy_id=split_item[0].strip(),
                                         taxonomy_term_id=split_item[1].strip()))
    return result


def validate_taxonomy_item(item):
    if item.find(' :') != -1 or item.find(': ') != -1:
        raise exceptions.ValidationError('"' + item + '" : Invalid taxonomy term format')

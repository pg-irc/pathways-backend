import json


def generate_task_fixture(tasks):
    header = ('// intended to be located at pathways-frontend/src/fixtures/tasks.ts\n'
              '\n'
              'import { Store } from \'./types/tasks\';\n'
              'export { Id, Task, TaskUserSettings, TaskMap, TaskUserSettingsMap, TaskList, Store } from \'./types/tasks\';\n'
              '\n'
              'export const buildTasksFixture = (): Store => {\n'
              '    return {\n'
              '        taskMap: ')

    footer = ('\n'
              '    }\n'
              '}')

    tasks_as_json = json.dumps(tasks, ensure_ascii=False, sort_keys=True, indent=4)

    return header + add_leading_spaces(8, tasks_as_json) + footer


def generate_taxonomy_fixture(taxonomies):
    header = ('export const buildTaxonomyFixture = (): Store => ({\n'
              '    taxonomyMap:     ')
    footer = ('\n);')
    taxonomies_as_dictionary = make_dict_from_taxonomies(taxonomies)
    taxonomies_as_json = json.dumps(taxonomies_as_dictionary,
                                    ensure_ascii=False,
                                    sort_keys=True,
                                    indent=4)
    return header + add_leading_spaces(4, taxonomies_as_json) + footer


def make_dict_from_taxonomies(taxonomies):
    result = {
        'explore':
        {
            'settlingIn': {'icon': 'sign-text'},
            'education': {'icon': 'book-open-variant'},
            'healthCare': {'icon': 'medical-bag'},
            'money': {'icon': 'currency-usd'},
            'housing': {'icon': 'home'},
            'employment': {'icon': 'briefcase'},
            'legalOrImmigration': {'icon': 'gavel'},
            'driving': {'icon': 'car'},
            'helpForIndividualsAndFamilies': {'icon': 'account'}
        }
    }

    for term in taxonomies:
        taxonomy_id = term.taxonomy_id
        ensure_map_has_key(result, taxonomy_id, {})

        term_id = term.taxonomy_term_id
        ensure_map_has_key(result[taxonomy_id], term_id, {'icon': 'unknown'})

    return result


def ensure_map_has_key(the_map, the_key, the_value):
    if the_key not in the_map:
        the_map[the_key] = the_value


def add_leading_spaces(count, tasks_as_json):
    json_lines = tasks_as_json.split('\n')
    json_lines_with_spaces = map(lambda line: count*' ' + line, json_lines)
    return '\n'.join(json_lines_with_spaces)

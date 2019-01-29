from django.test import TestCase
from newcomers_guide.generate_fixtures import (generate_task_fixture, generate_taxonomy_fixture)
from newcomers_guide.parse_data import TaxonomyTermReference


class GenerateFixtureTest(TestCase):
    def setUp(self):
        self.english_path = 'some/path/chapter/tasks/To_learn_english/en.Learn_english.txt'
        self.content = 'the content in English'

    def test_generated_task_fixture(self):
        self.maxDiff = None
        data = {
            'taskMap': {
                'To_learn_english': {
                    'completed': False,
                    'id': 'To_learn_english',
                    'title': {
                        'en': 'Learn_english'
                    },
                    'description': {
                        'en': 'the content in English'
                    }
                }
            }
        }
        expected = ('// intended to be located at pathways-frontend/src/fixtures/newcomers_guide/tasks.ts\n'
                    '// tslint:disable:quotemark trailing-comma max-line-length\n'
                    '\n'
                    'import { ValidTaskStore } from \'../types/tasks\';\n'
                    '\n'
                    'export const buildTasksFixture = (): ValidTaskStore => {\n'
                    '    return new ValidTaskStore({\n'
                    '        savedTasksList: [],\n'
                    '        taskMap: {\n'
                    '            "To_learn_english": {\n'
                    '                "completed": false,\n'
                    '                "description": {\n'
                    '                    "en": "the content in English"\n'
                    '                },\n'
                    '                "id": "To_learn_english",\n'
                    '                "title": {\n'
                    '                    "en": "Learn_english"\n'
                    '                }\n'
                    '            }\n'
                    '        }\n'
                    '    });\n'
                    '};')
        self.assertEqual(generate_task_fixture(data), expected)

    def test_generated_taxonomy_fixture(self):
        self.maxDiff = None
        data = [TaxonomyTermReference('TheTaxId', 'TheTaxTermId', 'topics', 'TheContentId')]
        expected = ('// intended to be located at pathways-frontend/src/fixtures/newcomers_guide/taxonomies.ts\n'
                    '// tslint:disable:quotemark trailing-comma max-line-length\n'
                    'import { TaxonomyStore } from \'../types/taxonomies\';\n'
                    '\n'
                    'export const buildTaxonomyFixture = (): TaxonomyStore => ({\n'
                    '    taxonomyMap:         {\n'
                    '        "TheTaxId": {\n'
                    '            "TheTaxTermId": {}\n'
                    '        },\n'
                    '        "explore": {\n'
                    '            "driving": {\n'
                    '                "icon": "car"\n'
                    '            },\n'
                    '            "education": {\n'
                    '                "icon": "graduation-cap"\n'
                    '            },\n'
                    '            "employment": {\n'
                    '                "icon": "briefcase"\n'
                    '            },\n'
                    '            "healthCare": {\n'
                    '                "icon": "heartbeat"\n'
                    '            },\n'
                    '            "helpForIndividualsAndFamilies": {\n'
                    '                "icon": "handshake-o"\n'
                    '            },\n'
                    '            "housing": {\n'
                    '                "icon": "building"\n'
                    '            },\n'
                    '            "legal": {\n'
                    '                "icon": "balance-scale"\n'
                    '            },\n'
                    '            "money": {\n'
                    '                "icon": "dollar"\n'
                    '            },\n'
                    '            "rightaway": {\n'
                    '                "icon": "briefcase"\n'
                    '            },\n'
                    '            "settling_in": {\n'
                    '                "icon": "street-view"\n'
                    '            }\n'
                    '        }\n'
                    '    }\n'
                    '});')

        self.assertEqual(generate_taxonomy_fixture(data), expected)

from django.test import TestCase
from newcomers_guide.generate_fixtures import generate_task_fixture, generate_taxonomy_fixture
from newcomers_guide.parse_data import TaxonomyTermReference


class GenerateFixtureTest(TestCase):
    def setUp(self):
        self.english_path = 'some/path/chapter/tasks/To_learn_english/en.Learn_english.txt'
        self.content = 'the content in English'

    def test_generated_task_fixture(self):
        self.maxDiff = None
        data = {
            'To_learn_english': {
                'id': 'To_learn_english',
                'title': {
                    'en': 'Learn_english'
                },
                'description': {
                    'en': 'the content in English'
                }
            }
        }
        expected = ('// intended to be located at pathways-frontend/src/fixtures/newcomers_guide/tasks.ts\n'
                    '// tslint:disable:quotemark trailing-comma max-line-length\n'
                    '\n'
                    'import { Store } from \'../types/tasks\';\n'
                    '\n'
                    'export const buildTasksFixture = (): Store => {\n'
                    '    return {\n'
                    '        taskUserSettingsMap: {},\n'
                    '        savedTasksList: [],\n'
                    '        suggestedTasksList: [],\n'
                    '        taskMap:         {\n'
                    '            "To_learn_english": {\n'
                    '                "description": {\n'
                    '                    "en": "the content in English"\n'
                    '                },\n'
                    '                "id": "To_learn_english",\n'
                    '                "title": {\n'
                    '                    "en": "Learn_english"\n'
                    '                }\n'
                    '            }\n'
                    '        }\n'
                    '    };\n'
                    '};')
        self.assertEqual(generate_task_fixture(data), expected)

    def test_generated_taxonomy_fixture(self):
        self.maxDiff = None
        data = [TaxonomyTermReference('TheTaxId', 'TheTaxTermId', 'tasks', 'TheContentId')]
        expected = ('// intended to be located at pathways-frontend/src/fixtures/newcomers_guide/taxonomies.ts\n'
                    '// tslint:disable:quotemark trailing-comma max-line-length\n'
                    'import { Store } from \'../types/taxonomies\';\n'
                    '\n'
                    'export const buildTaxonomyFixture = (): Store => ({\n'
                    '    taxonomyMap:         {\n'
                    '        "TheTaxId": {\n'
                    '            "TheTaxTermId": {}\n'
                    '        },\n'
                    '        "explore": {\n'
                    '            "driving": {\n'
                    '                "icon": "car"\n'
                    '            },\n'
                    '            "education": {\n'
                    '                "icon": "book-open-variant"\n'
                    '            },\n'
                    '            "employment": {\n'
                    '                "icon": "briefcase"\n'
                    '            },\n'
                    '            "healthCare": {\n'
                    '                "icon": "medical-bag"\n'
                    '            },\n'
                    '            "helpForIndividualsAndFamilies": {\n'
                    '                "icon": "account"\n'
                    '            },\n'
                    '            "housing": {\n'
                    '                "icon": "home"\n'
                    '            },\n'
                    '            "legalOrImmigration": {\n'
                    '                "icon": "gavel"\n'
                    '            },\n'
                    '            "money": {\n'
                    '                "icon": "currency-usd"\n'
                    '            },\n'
                    '            "settlingIn": {\n'
                    '                "icon": "sign-text"\n'
                    '            }\n'
                    '        }\n'
                    '    }\n'
                    '});')

        self.assertEqual(generate_taxonomy_fixture(data), expected)

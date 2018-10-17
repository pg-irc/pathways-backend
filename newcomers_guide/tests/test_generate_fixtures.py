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
        data = [TaxonomyTermReference('TheTaxId', 'TheTaxTermId', 'tasks', 'TheContentId')]
        expected = ('// intended to be located at pathways-frontend/src/fixtures/newcomers_guide/taxonomies.ts\n'
                    '// tslint:disable:quotemark trailing-comma max-line-length\n'
                    'import { TaxonomyStore } from \'../types/taxonomies\';\n'
                    '\n'
                    'export const buildTaxonomyFixture = (): TaxonomyStore => ({\n'
                    '    taxonomyMap:         {\n'
                    '        "TheTaxId": {\n'
                    '            "TheTaxTermId": {}\n'
                    '        },\n'
                    '        "age": {\n'
                    '            "13_to_18": {},\n'
                    '            "18_to_64": {},\n'
                    '            "over_65": {},\n'
                    '            "under_13": {}\n'
                    '        },\n'
                    '        "english_level": {\n'
                    '            "beginner": {},\n'
                    '            "fluent": {},\n'
                    '            "intermediate": {},\n'
                    '            "none": {}\n'
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
                    '            "legal": {\n'
                    '                "icon": "gavel"\n'
                    '            },\n'
                    '            "money": {\n'
                    '                "icon": "currency-usd"\n'
                    '            },\n'
                    '            "settling_in": {\n'
                    '                "icon": "sign-text"\n'
                    '            }\n'
                    '        },\n'
                    '        "group": {\n'
                    '            "disability": {},\n'
                    '            "lgbtq2": {},\n'
                    '            "low_income": {},\n'
                    '            "services_in_french": {},\n'
                    '            "women": {}\n'
                    '        },\n'
                    '        "immigrant_type": {\n'
                    '            "permanent_resident": {},\n'
                    '            "refugee_claimant": {},\n'
                    '            "temporary_resident": {},\n'
                    '            "unknown": {}\n'
                    '        },\n'
                    '        "refugee_claim_stage": {\n'
                    '            "claim_at_border": {},\n'
                    '            "claim_at_cic_office": {},\n'
                    '            "hearing": {},\n'
                    '            "negative_decision": {},\n'
                    '            "not_started": {},\n'
                    '            "positive_decision": {}\n'
                    '        },\n'
                    '        "time_in_canada": {\n'
                    '            "not_yet_arrived": {},\n'
                    '            "over_2_years": {},\n'
                    '            "under_1_month": {},\n'
                    '            "under_1_year": {},\n'
                    '            "under_2_years": {},\n'
                    '            "under_6_months": {}\n'
                    '        },\n'
                    '        "user": {\n'
                    '            "alone": {},\n'
                    '            "with_family": {}\n'
                    '        }\n'
                    '    }\n'
                    '});')

        self.assertEqual(generate_taxonomy_fixture(data), expected)

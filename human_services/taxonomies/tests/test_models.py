from django.core import exceptions
from django.db import IntegrityError
from django.test import TestCase
from human_services.taxonomies import models
from human_services.taxonomies.tests.helpers import TaxonomyTermBuilder


def validate_save_and_reload(taxonomy_term):
    taxonomy_term.save()
    return models.TaxonomyTerm.objects.get(pk=taxonomy_term.pk)


class TestTaxonomyModel(TestCase):
    def test_has_taxonomy_id_field(self):
        taxonomy_id = 'the_taxonomy_id'
        taxonomy_term = TaxonomyTermBuilder().with_taxonomy_id(taxonomy_id).build()
        taxonomy_term_from_db = validate_save_and_reload(taxonomy_term)
        self.assertEqual(taxonomy_term_from_db.taxonomy_id, taxonomy_id)

    def test_taxonomy_id_cannot_be_none(self):
        taxonomy_id = None
        taxonomy_term = TaxonomyTermBuilder().with_taxonomy_id(taxonomy_id).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_taxonomy_id_cannot_be_empty(self):
        taxonomy_id = ''
        taxonomy_term = TaxonomyTermBuilder().with_taxonomy_id(taxonomy_id).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_taxonomy_id_cannot_contain_space(self):
        taxonomy_id = 'the taxonomy_id'
        taxonomy_term = TaxonomyTermBuilder().with_taxonomy_id(taxonomy_id).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_has_name_field(self):
        name = 'the_name'
        taxonomy_term = TaxonomyTermBuilder().with_name(name).build()
        taxonomy_term_from_db = validate_save_and_reload(taxonomy_term)
        self.assertEqual(taxonomy_term_from_db.name, name)

    def test_name_cannot_be_none(self):
        name = None
        taxonomy_term = TaxonomyTermBuilder().with_name(name).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_name_cannot_be_empty(self):
        name = ''
        taxonomy_term = TaxonomyTermBuilder().with_name(name).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_name_cannot_contain_space(self):
        name = 'the name'
        taxonomy_term = TaxonomyTermBuilder().with_name(name).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    # pylint: disable=invalid-name
    def test_saving_two_taxonomies_with_same_taxonomy_id_and_different_name(self):
        taxonomy_id = 'the_taxonomy_id'
        name_1 = 'the_name_1'
        name_2 = 'the_name_2'

        taxonomy_term1 = TaxonomyTermBuilder().with_taxonomy_id(taxonomy_id).build()
        taxonomy_term1.name = name_1
        taxonomy_term1.save()

        taxonomy_term2 = TaxonomyTermBuilder().with_taxonomy_id(taxonomy_id).build()
        taxonomy_term2.name = name_2
        taxonomy_term2.save()

        self.assertNotEqual(taxonomy_term1.pk, taxonomy_term2.pk)

    # pylint: disable=invalid-name
    def test_saving_two_taxonomies_with_same_name_and_different_taxonomy_id(self):
        taxonomy_id_1 = 'the_taxonomy_id_1'
        taxonomy_id_2 = 'the_taxonomy_id_2'
        name = 'the_name'

        taxonomy_term1 = TaxonomyTermBuilder().with_name(name).build()
        taxonomy_term1.taxonomy_id = taxonomy_id_1
        taxonomy_term1.save()

        taxonomy_term2 = TaxonomyTermBuilder().with_name(name).build()
        taxonomy_term2.taxonomy_id = taxonomy_id_2
        taxonomy_term2.save()

        self.assertNotEqual(taxonomy_term1.pk, taxonomy_term2.pk)

    # pylint: disable=invalid-name
    def test_saving_two_taxonomies_with_same_name_and_taxonomy_id_fails_with_integrity_error(self):
        taxonomy_id = 'the_taxonomy_id'
        name = 'the_name'

        taxonomy_term1 = TaxonomyTermBuilder().with_taxonomy_id(taxonomy_id).with_name(name).build()
        taxonomy_term1.save()

        taxonomy_term2 = TaxonomyTermBuilder().with_taxonomy_id(taxonomy_id).with_name(name).build()
        with self.assertRaises(IntegrityError):
            taxonomy_term2.save()

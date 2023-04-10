from django.core.exceptions import ValidationError
from django.test import TestCase

from shop.models import Section, Product


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Section.objects.create(title='Main', slug='main')
        Product.objects.create(
            title='Title', slug='title',
            section=Section.objects.get(id=1),
            price=200,
            year=2000,
            country='Россия',
            director='Режиссёр',
            cast='Актёры',
            description='Описание фильма'
        )

    def test_section_null(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('section').null)

    def test_image_upload_to(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('image').upload_to, 'images')

    def test_year(self):
        obj = Product.objects.get(id=1)
        obj.year = 1500
        self.assertRaises(ValidationError, obj.full_clean)
        obj.year = 3000
        self.assertRaises(ValidationError, obj.full_clean)

    def test_meta_ordering(self):
        obj = Product.objects.get(id=1)
        ordering = obj._meta.ordering
        self.assertEqual(ordering, ['title', '-year'])

    def test_count(self):
        obj = Product.objects.get(id=1)
        obj.count = 5
        self.assertEqual(obj.get_count(), 5)

    def test_get_sum_price(self):
        obj = Product.objects.get(id=1)
        obj.count = 2
        self.assertEqual(obj.get_sum_price(), 400)

    def test_str(self):
        obj = Product.objects.get(id=1)
        self.assertEqual(str(obj), 'Title (Main)')

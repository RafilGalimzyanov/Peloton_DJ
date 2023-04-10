from django.core.exceptions import ValidationError
from django.test import TestCase

from shop.models import Discount


class DiscountModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Discount.objects.create(code='ABC', value=50)

    def test_title_max_length(self):
        obj = Discount.objects.get(id=1)
        max_length = obj._meta.get_field('code').max_length
        self.assertEqual(max_length, 10)

    def test_value(self):
        obj = Discount.objects.get(id=1)
        obj.value = -10
        self.assertRaises(ValidationError, obj.full_clean)
        obj.value = 110
        self.assertRaises(ValidationError, obj.full_clean)

    def test_str(self):
        obj = Discount.objects.get(id=1)
        self.assertEqual(str(obj), 'ABC (50%)')

    def test_value_percent_short_description(self):
        obj = Discount.objects.get(id=1)
        short_description = obj.value_percent.short_description
        self.assertEqual(short_description, 'Размер скидки')
from django.test import TestCase

from shop.forms import SearchForm, OrderModelForm
from shop.models import Order


class SearchFormTest(TestCase):

    def test_q_placeholder(self):
        form = SearchForm()
        self.assertEqual(form.fields['q'].widget.attrs['placeholder'], 'Поиск')


class OrderFormTest(TestCase):

    def test_delivery_choices(self):
        DELIVERY_CHOICES = [
            (0, 'Выберите, пожалуйста'),
            (1, 'Доставка'),
            (2, 'Самовывоз'),
        ]
        form = OrderModelForm()
        self.assertEqual(form.fields['delivery'].choices, DELIVERY_CHOICES)

    def test_delivery_label(self):
        form = OrderModelForm()
        self.assertEqual(form.fields['delivery'].label, 'Доставка')

    def test_delivery_coerce(self):
        form = OrderModelForm()
        self.assertEqual(form.fields['delivery'].coerce, int)

    def test_meta_model(self):
        form = OrderModelForm()
        self.assertEqual(form._meta.model, Order)

    def test_meta_exclude(self):
        form = OrderModelForm()
        self.assertEqual(form._meta.exclude, ['discount', 'status', 'need_delivery'])

    def test_meta_labels(self):
        form = OrderModelForm()
        self.assertEqual(form._meta.labels, {'address': 'Полный адрес (Страна, город, индекс, улица, дом, квартира)'})

    def test_address_rows(self):
        form = OrderModelForm()
        self.assertEqual(form._meta.widgets['address'].attrs['rows'], 6)

    def test_notice_cols(self):
        form = OrderModelForm()
        self.assertEqual(form.fields['notice'].widget.attrs['cols'], 80)

    def test_valid_delivery_0(self):
        data = {'name': 'Имя', 'email': 'abc@example.com', 'phone': '3123455', 'address': 'Адрес', 'delivery': 0}
        form = OrderModelForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_delivery_1_without_address(self):
        data = {'name': 'Имя', 'email': 'abc@example.com', 'phone': '3123455', 'address': '', 'delivery': 1}
        form = OrderModelForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_delivery_1_with_address(self):
        data = {'name': 'Имя', 'email': 'abc@example.com', 'phone': '3123455', 'address': 'Адрес', 'delivery': 1}
        form = OrderModelForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_delivery_2(self):
        data = {'name': 'Имя', 'email': 'abc@example.com', 'phone': '3123455', 'address': '', 'delivery': 2}
        form = OrderModelForm(data=data)
        self.assertTrue(form.is_valid())
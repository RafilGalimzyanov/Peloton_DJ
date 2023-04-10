from django.test import TestCase

from shop.models import Section, Product, Order, OrderLine


class OrderLineModelTest(TestCase):

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
        Order.objects.create(
            need_delivery=False,
            name='Имя',
            phone='3235235',
            email='abc@example.com',
            address=''
        )
        OrderLine.objects.create(
            order=Order.objects.get(id=1),
            product=Product.objects.get(id=1),
            price=Product.objects.get(id=1).price,
            count=5
        )

    def test_price_max_digits(self):
        obj = OrderLine.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('price').max_digits, 10)

    def test_str(self):
        obj = OrderLine.objects.get(id=1)
        self.assertTrue(str(obj), 'Заказ (ID 1) Title: 5 шт.')

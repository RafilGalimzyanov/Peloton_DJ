from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from shop.models import Section, Product, OrderLine, Order


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Section.objects.create(title='Main', slug='main')
        for i in range(30):
            Product.objects.create(
                title='Title ' + str(i), slug='title-' + str(i),
                section=Section.objects.get(id=1),
                image='abc.jpg',
                price=200,
                year=2000,
                country='Россия',
                director='Режиссёр',
                cast='Актёры',
                description='Интересный фильм'
            )

    def test_200(self):
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/shop/')
        self.assertTemplateUsed(response, 'index.html')

    def test_context(self):
        response = self.client.get('/shop/')
        self.assertEqual(len(response.context['products']), 8)


class AddCartViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Section.objects.create(title='Main', slug='main')
        for i in range(30):
            Product.objects.create(
                title='Title ' + str(i), slug='title-' + str(i),
                section=Section.objects.get(id=1),
                image='abc.jpg',
                price=200,
                year=2000,
                country='Россия',
                director='Режиссёр',
                cast='Актёры',
                description='Интересный фильм'
            )

    def test_302(self):
        response = self.client.get('/shop/?add_cart=1')
        self.assertEqual(response.status_code, 302)

    def test_cart_info(self):
        self.client.get('/shop/?add_cart=1')
        self.client.get('/shop/?add_cart=1')
        self.assertEqual(self.client.session['cart_info'], {'1': 2})

    def test_404(self):
        response = self.client.get('/shop/?add_cart=100')
        self.assertEqual(response.status_code, 404)


class OrdersViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Section.objects.create(title='Main', slug='main')
        for i in range(30):
            Product.objects.create(
                title='Title ' + str(i), slug='title-' + str(i),
                section=Section.objects.get(id=1),
                image='abc.jpg',
                price=200,
                year=2000,
                country='Россия',
                director='Режиссёр',
                cast='Актёры',
                description='Интересный фильм'
            )
        User.objects.create_user(username='abc@example.com', email='abc@example.com', password='123456')
        order = Order.objects.create(
            need_delivery=False,
            name='Имя клиента',
            phone='523523532',
            email='abc@example.com',
            address=''
        )
        OrderLine.objects.create(
            order=order,
            product=Product.objects.get(id=1),
            price=Product.objects.get(id=1).price,
            count=5
        )

    def test_redirect_not_logged(self):
        response = self.client.get(reverse('orders'))
        self.assertRedirects(response, '/accounts/login/?next=/shop/orders')

    def test_login(self):
        self.client.login(username='abc@example.com', password='123456')
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.context['user'].username, 'abc@example.com')

    def test_template(self):
        self.client.login(username='abc@example.com', password='123456')
        response = self.client.get(reverse('orders'))
        self.assertTemplateUsed(response, 'orders.html')

    def test_orders(self):
        self.client.login(username='abc@example.com', password='123456')
        response = self.client.get(reverse('orders'))
        self.assertEqual(len(response.context['orders']), 1)
        self.assertEqual(response.context['orders'][0].id, 1)


class OrderViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='Клиенты')
        Section.objects.create(title='Main', slug='main')
        for i in range(30):
            Product.objects.create(
                title='Title ' + str(i), slug='title-' + str(i),
                section=Section.objects.get(id=1),
                image='abc.jpg',
                price=200,
                year=2000,
                country='Россия',
                director='Режиссёр',
                cast='Актёры',
                description='Интересный фильм'
            )

    def test_404(self):
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 404)

    def test_200(self):
        self.client.get('/shop/?add_cart=1')
        self.client.get('/shop/?add_cart=1')
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)

    def test_name(self):
        self.client.get('/shop/?add_cart=1')
        self.client.get('/shop/?add_cart=1')
        data = {'name': '', 'email': 'abc@example.com', 'phone': '325325', 'address': '', 'delivery': 2}
        response = self.client.post(reverse('order'), data)
        self.assertFormError(response, 'form', 'name', 'Обязательное поле.')

    def test_delivery(self):
        self.client.get('/shop/?add_cart=1')
        self.client.get('/shop/?add_cart=1')
        data = {'name': 'Имя', 'email': 'abc@example.com', 'phone': '325325', 'address': '', 'delivery': 0}
        response = self.client.post(reverse('order'), data)
        self.assertFormError(response, 'form', 'delivery', 'Необходимо выбрать способ доставки')

    def test_address(self):
        self.client.get('/shop/?add_cart=1')
        self.client.get('/shop/?add_cart=1')
        data = {'name': 'Имя', 'email': 'abc@example.com', 'phone': '325325', 'address': '', 'delivery': 1}
        response = self.client.post(reverse('order'), data)
        self.assertEqual(response.context['form'].non_field_errors(), ['Укажите адрес доставки'])

    def test_add_user(self):
        self.client.get('/shop/?add_cart=1')
        self.client.get('/shop/?add_cart=1')
        data = {'name': 'Имя', 'email': 'abc@example.com', 'phone': '325325', 'address': '', 'delivery': 2}
        self.client.post(reverse('order'), data)
        user = User.objects.get(email='abc@example.com')
        self.assertEqual(user.username, 'abc@example.com')

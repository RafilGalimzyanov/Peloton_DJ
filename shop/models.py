import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import TextField
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Section(models.Model):
    title = models.CharField(
        max_length=70,
        help_text='Тут надо ввести название раздела',
        unique=True,
        verbose_name='Название раздела'
    )
    slug = models.SlugField(max_length=40, verbose_name='Псевдоним', default='')

    class Meta:
        ordering = ['id']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def get_absolute_url(self):
        return reverse('section', args=[self.slug])

    def __str__(self):
        return self.title


class Product(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, verbose_name='Раздел')
    title = models.CharField(max_length=70, verbose_name='Название')
    slug = models.SlugField(max_length=40, verbose_name='Псевдоним', default='')
    image = models.ImageField(upload_to='images', verbose_name='Изображение')
    ves = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Вес',
        help_text='гр.')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    year = models.IntegerField(
        validators=[MinValueValidator(30)],
        verbose_name='Срок годности',
         help_text ='В днях'
    )
    country = models.CharField(max_length=70, verbose_name='Страна')
    play = models.IntegerField(

        null=True,
        blank=True,
        verbose_name='Количество в упаковке',
        help_text='В шт.'
    )
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

    count = 1

    class Meta:
        ordering = ['title', '-year']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_count(self):
        return self.count

    def get_sum_price(self):
        return self.count * self.price

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.section.title)


class Discount(models.Model):
    code = models.CharField(max_length=10, verbose_name='Код купона')
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Размер скидки',
        help_text='В процентах'
    )

    class Meta:
        ordering = ['-value']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def value_percent(self):
        return str(self.value) + '%'

    def __str__(self):
        return self.code + ' (' + str(self.value) + '%)'

    value_percent.short_description = 'Размер скидки'


class Order(models.Model):
    need_delivery = models.BooleanField(verbose_name='Необходима доставка')
    discount = models.ForeignKey(Discount, verbose_name='Скидка', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=70, verbose_name='Имя')
    surname = models.CharField(max_length=70, verbose_name='Фамилия')
    phone = models.CharField(max_length=11, null=False, blank=False, verbose_name='Телефон', )
    email = models.EmailField()
    address = models.TextField(blank=True, verbose_name='Адрес')
    notice = models.TextField(blank=True, verbose_name='Примечание к заказу')
    date_order = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    date_send = models.DateTimeField(null=True, blank=True, verbose_name='Дата отправки')
    date_delivery = models.CharField(max_length=40, verbose_name='Время доставки')

    STATUSES = [
        ('NEW', 'Новый заказ'),
        ('APR', 'Подтверждён'),
        ('PAY', 'Оплачен'),
        ('CNL', 'Отменён')
    ]

    status = models.CharField(choices=STATUSES, max_length=3, default='NEW', verbose_name='Статус')

    class Meta:
        ordering = ['-date_order']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        permissions = (('can_set_status', 'Возможность настройки статуса'), )

    def display_products(self):
        display = ''
        for order_line in self.orderline_set.all():
            display += '{0}: {1} шт.; '.format(order_line.product.title, order_line.count)
        return display

    def display_amount(self):
        amount = 0
        for order_line in self.orderline_set.all():
            amount += order_line.price * order_line.count

        if self.discount:
            amount = round(amount * Decimal(1 - self.discount.value / 100))
        return '{0} руб.'.format(amount)

    def __str__(self):
        return 'ID: ' + str(self.id)

    display_products.short_description = 'Состав заказа'
    display_amount.short_description = 'Сумма'


class OrderLine(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    count = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(1)], default=1)

    class Meta:
        verbose_name = 'Строка заказа'
        verbose_name_plural = 'Строки заказов'

    def __str__(self):
        return 'Заказ (ID {0}) {1}: {2} шт.'.format(self.order.id, self.product.title, self.count,)


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100, verbose_name='Имя')
    rev = models.TextField(blank=True, verbose_name='Отзыв')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Job(models.Model):
    vakancy = models.CharField(max_length=70, verbose_name='Название вакансии')
    opit = models.BooleanField(verbose_name='Опыт работы')
    obyazanosti = models.TextField(max_length=300, verbose_name='Обязанности', null=True)
    trebovaniya = models.TextField(max_length=300, verbose_name='Требования')
    usloviya = models.TextField(max_length=300, verbose_name='Условия труда')
    zp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Зарплата', default=0)

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
from django.contrib import admin

from shop.models import Section, Product, Discount, Order, OrderLine, Review, Job

admin.site.register(Section)
# admin.site.register(Product)
# admin.site.register(Discount)
# admin.site.register(Order)
# admin.site.register(OrderLine)


class PriceFilter(admin.SimpleListFilter):
    title = 'Цена'
    parameter_name = 'price'
    round_value = 100

    def lookups(self, request, model_admin):
        """
        return (
            ('100', '0 - 100'),
            ('200', '101 - 200'),
            ('300', '201 - 300'),
            ('400', '301 - 400'),
        )
        """
        filters = []
        product = Product.objects.order_by('price').last()
        if product:
            # print(product.price)
            max_price = round(product.price / self.round_value) * self.round_value + self.round_value
            price = self.round_value
            while price <= max_price:
                start = price
                start_price = price - self.round_value
                if start_price != 0:
                    start_price += 1
                end = '{0} - {1}'.format(start_price, price)
                filters.append((start, end))
                price += self.round_value
        return filters

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        value = int(self.value())
        return queryset.filter(price__gte=(value - self.round_value + 1), price__lte=value)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'section', 'image', 'price', 'date')
    # list_filter = ('section', 'price')
    list_filter = ('section', PriceFilter)
    actions_on_bottom = True
    # actions_on_top = False
    list_per_page = 10
    search_fields = ('title', 'cast')


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'value_percent')

    def save_model(self, request, obj, form, change):
        print('Request', request)
        print('Obj', obj)
        print('Form', form)
        print('Change', change)
        super(DiscountAdmin, self).save_model(request, obj, form, change)
        print('Request', request)
        print('Obj', obj)
        print('Form', form)
        print('Change', change)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'display_products', 'display_amount',
        'name', 'surname', 'discount', 'phone',
        'email', 'address', 'notice',
        'date_order', 'date_send', 'status', 'date_delivery',
    )
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('need_delivery', 'discount')
        }),
        ('Информация о клиенте', {
            'fields': ('name','surname', 'phone', 'email', 'address'),
            'description': 'Контактная информация'
        }),
        ('Доставка и оплата', {
            'fields': ('date_send', 'status')
        })
    )
    list_filter = ('status', 'date_order')
    date_hierarchy = 'date_order'


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order',  'product', 'price', 'count',)
    list_filter = ('order',)


class reviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rev',)

class jobAdmin(admin.ModelAdmin):
    list_display = ('vakancy', 'opit', 'trebovaniya', 'usloviya', 'zp',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Job, jobAdmin)
admin.site.register(Review, reviewAdmin)
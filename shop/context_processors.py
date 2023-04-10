from decimal import Decimal

from shop.forms import SearchForm
from shop.models import Section, Product, Discount


def add_default_data(request):
    sections = Section.objects.all().order_by('title')
    search_form = SearchForm()
    count_in_cart = 0
    sum_in_cart = 0
    cart_info = request.session.get('cart_info', {})
    for key in cart_info:
        count_in_cart += cart_info[key]
        sum_product = Product.objects.get(pk=key).price * cart_info[key]
        sum_in_cart += sum_product
    try:
        discount_code = request.session.get('discount', '')
        discount = Discount.objects.get(code__exact=discount_code)
        if discount:
            sum_in_cart = round(sum_in_cart * Decimal(1 - discount.value / 100))
    except Discount.DoesNotExist:
        pass

    return {
        'sections': sections, 'search_form': search_form,
        'count_in_cart': count_in_cart, 'sum_in_cart': sum_in_cart
    }

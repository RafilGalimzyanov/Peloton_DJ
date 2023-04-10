# import transliterate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import generic

from shop.forms import SearchForm, OrderModelForm, ReviewForm
from shop.models import Section, Product, Discount, Order, OrderLine, Review, Job


def index(request):
    """
    products = Product.objects.all()
    for product in products:
        slug = transliterate.translit(product.title, reversed=True)
        slug = slug.replace("'", '')
        slug = slug.replace('?', '')
        slug = slug.replace(',', '')
        slug = slug.replace(' ', '-')
        slug = slug.lower()
        product.slug = slug
        product.save()
        # print(slug)
    """
    result = prerender(request)
    if result:
        return result
    products = Product.objects.all().order_by(get_order_by_products(request))[:8]
    context = {'products': products}
    return render(
        request,
        'index.html',
        context=context
    )


def prerender(request):
    if request.GET.get('add_cart'):
        product_id = request.GET.get('add_cart')
        get_object_or_404(Product, pk=product_id)
        cart_info = request.session.get('cart_info', {})
        count = cart_info.get(product_id, 0)
        count += 1
        cart_info.update({product_id: count})
        request.session['cart_info'] = cart_info
        # print(cart_info)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def get_order_by_products(request):
    order_by = ''
    if request.GET.__contains__('sort') and request.GET.__contains__('up'):
        sort = request.GET['sort']
        up = request.GET['up']
        if sort == 'price' or sort == 'title':
            if up == '0':
                order_by = '-'
            order_by += sort
    if not order_by:
        order_by = '-date'
    return order_by


def delivery(request):
    return render(
        request,
        'delivery.html'
    )


def contacts(request):
    return render(
        request,
        'contacts.html'
    )


def peloton(request):
    return render(
        request,
        'peloton.html'
    )


def review(request):
    review_form = ReviewForm()
    all_reviews = Review.objects.all()
    context = {
        'reviews': all_reviews,
    }
    if request.user.is_authenticated:
        context.update({"form": review_form})

    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        rev = request.POST.get("rev")

        rev_model = Review(email=email, name=name, rev=rev)
        rev_model.save()

    return render(
        request,
        'reviews.html',
        context=context,
    )


def job(request):
    all_jobs = Job.objects.all()
    context = {
        'jobs': all_jobs,
    }
    return render(
        request,
         'job.html',
        context=context,
     )



#def section(request, id):
def section(request, slug):
    result = prerender(request)
    if result:
        return result
    #obj = Section.objects.get(pk=id)
    obj = get_object_or_404(Section, slug=slug)
    products = Product.objects.filter(section__exact=obj).order_by(get_order_by_products(request))
    context = {'section': obj, 'products': products}
    return render(
        request,
        'section.html',
        context=context
    )


class ProductDetailView(generic.DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        result = prerender(request)
        if result:
            return result
        return super(ProductDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.\
                                  filter(section__exact=self.get_object().section).\
                                  exclude(id=self.get_object().id).order_by('?')[:4]
        return context


def handler404(request, exception):
    return render(request, '404.html', status=404)


def search(request):
    result = prerender(request)
    if result:
        return result
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.cleaned_data['q']
        products = Product.objects.filter(
            Q(title__icontains=q) | Q(country__icontains=q)| Q(description__icontains=q)
        )
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 4)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context = {'products': products, 'q': q}
        return render(
            request,
            'search.html',
            context=context
        )


def cart(request):
    result = update_cart_info(request)
    if result:
        return result
    cart_info = request.session.get('cart_info')
    products = []
    if cart_info:
        for product_id in cart_info:
            #product = get_object_or_404(Product, pk=product_id)
            try:
                product = Product.objects.get(pk=product_id)
                product.count = cart_info[product_id]
                products.append(product)
            except Product.DoesNotExists:
                raise Http404()
    context = {'products': products, 'discount': request.session.get('discount', '')}
    return render(
        request,
        'cart.html',
        context=context
    )


def update_cart_info(request):
    if request.POST:
        cart_info = {}
        for param in request.POST:
            value = request.POST.get(param)
            # print(param, value)
            if param.startswith('count_') and value.isnumeric():
                product_id = param.replace('count_', '')
                get_object_or_404(Product, pk=product_id)
                cart_info[product_id] = int(value)
            elif param == 'discount' and value:
                try:
                    discount = Discount.objects.get(code__exact=value)
                    request.session['discount'] = value
                except Discount.DoesNotExist:
                    pass

        request.session['cart_info'] = cart_info

    if request.GET.get('delete_cart'):
        cart_info = request.session.get('cart_info')
        product_id = request.GET.get('delete_cart')
        get_object_or_404(Product, pk=product_id)
        current_count = cart_info.get(product_id, 0)
        if current_count == 1:
            cart_info.pop(product_id)
        elif current_count == 0:
            raise Http404()
        else:
            cart_info[product_id] -= 1
        request.session['cart_info'] = cart_info
        return HttpResponseRedirect(reverse('cart'))
    # print('discount =', request.session.get('discount', ''))


def order(request):
    DELIVERY_TIME = (
        '8:00-10:00',
        '11:00-13:00',
        '14:00-16:00',
        '17:00-20:00',
    )
    cart_info = request.session.get('cart_info')
    if not cart_info:
        raise Http404()
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order_obj = Order()
            order_obj.need_delivery = True if form.cleaned_data['delivery'] == 1 else False
            discount_code = request.session.get('discount', '')
            if discount_code:
                try:
                    discount = Discount.objects.get(code__exact=discount_code)
                    order_obj.discount = discount
                except Discount.DoesNotExist:
                    pass
            order_obj.name = form.cleaned_data['name']
            order_obj.surname = form.cleaned_data['surname']
            order_obj.phone = form.cleaned_data['phone']
            order_obj.email = form.cleaned_data['email']
            order_obj.address = form.cleaned_data['address']
            order_obj.notice = form.cleaned_data['notice']
            order_obj.date_delivery = DELIVERY_TIME[form.cleaned_data['time_delivery']-1]
            order_obj.save()
            add_order_lines(request, order_obj)
            add_user(form.cleaned_data['name'], form.cleaned_data['surname'], form.cleaned_data['email'])
            print([i.date_delivery for i in Order.objects.all()])
            return HttpResponseRedirect(reverse('addorder'))
        else:
            print(form.errors)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {'name': request.user.first_name, 'surname': request.user.last_name, 'email': request.user.email, }
        form = OrderModelForm(initial=initial)

    context = {'form': form}
    return render(
        request,
        'order.html',
        context=context
    )


def add_order_lines(request, order_obj):
    cart_info = request.session.get('cart_info', {})
    for key in cart_info:
        order_line = OrderLine()
        order_line.order = order_obj
        order_line.product = get_object_or_404(Product, pk=key)
        order_line.price = order_line.product.price
        order_line.count = cart_info[key]
        order_line.save()
    del request.session['cart_info']
    # request.session.clear() # Стирает слишком много, в том числе и авторизацию


def addorder(request):
    return render(
        request,
        'addorder.html'
    )


def add_user(name, surname, email):
    if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
        return
    password = User.objects.make_random_password()
    user = User.objects.create_user(email, email, password)
    user.first_name = name
    user.last_name = surname
    group = Group.objects.get(name='Клиенты')
    user.groups.add(group)
    user.save()

    text = get_template('registration/registration_email.html')
    html = get_template('registration/registration_email.html')

    context = {'username': email, 'password': password}

    subject = 'Регистрация'
    from_email = 'from@peloton.ru'
    text_content = text.render(context)
    html_content = html.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@login_required
def orders(request):
    user_orders = Order.objects.filter(email__exact=request.user.email)
    return render(
        request,
        'orders.html',
        context={'orders': user_orders}
    )


@permission_required('shop.can_set_status')
def cancelorder(request, id):
    print(request.user.has_perm('shop.can_set_status'))
    order_obj = get_object_or_404(Order, pk=id)
    if order_obj.email == request.user.email and order_obj.status == 'NEW':
        order_obj.status = 'CNL'
        order_obj.save()
    return HttpResponseRedirect(reverse('orders'))





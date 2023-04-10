from django.urls import path, re_path

from shop import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('delivery', views.delivery, name='delivery'),
    path('contacts', views.contacts, name='contacts'),
    #url(r'^section/(?P<id>\d+)$', views.section, name='section'),
    path('section/<slug:slug>', views.section, name='section'),
    # url(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product'),
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product'),
    path('search', views.search, name='search'),
    path('cart', views.cart, name='cart'),
    path('order', views.order, name='order'),
    path('addorder', views.addorder, name='addorder'),
    path('orders', views.orders, name='orders'),
   re_path(r'^cancelorder/(?P<id>\d+)$', views.cancelorder, name='cancelorder'),
    path('', views.peloton, name='peloton'),
    path('reviews', views.review, name='reviews'),
    path('job', views.job, name='job'),
]

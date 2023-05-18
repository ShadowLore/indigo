from django.urls import path
from . import views
from cart.views import Cart, add_to_cart, remove_from_cart, CartView, decreaseCart


from .views import (
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,

    Redac,

    CategoryCreateView,
    CategoryDeleteView,
    CategoryUpdateView,
    CategoryDetailView,
)

app_name = 'mainapp'

urlpatterns = [
    path('', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('about_delivery/', views.about_delivery, name='about_delivery'),
    path('contacts/', views.contacts, name='contacts'),

    path('cart/', CartView, name='cart-home'),
    path('catalog/', views.category, name='catalog'),

    path('cart/<slug>', add_to_cart, name='cart'),
    path('remove/<slug>', remove_from_cart, name='remove-cart'),

    path('decrease-cart/<slug>', decreaseCart, name='decrease-cart'),

    path('redac/', Redac.as_view(), name='redac'),

    path('catalog/<slug>', ProductDetailView.as_view(), name='product-detail'),

    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<slug>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<slug>/delete/', ProductDeleteView.as_view(), name='product-delete'),


    path('category/new/', CategoryCreateView.as_view(), name='category-create'),
    path('category/<slug>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<slug>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('search/', views.search, name='search'),

    path('catalog/<int:pk>/<str:slug>/', CategoryDetailView.as_view(), name='category')
]
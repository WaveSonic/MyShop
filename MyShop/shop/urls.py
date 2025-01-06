from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('category/<str:category>', views.category_list, name='category_list'),
    path('product/<int:product_id>', views.product, name='product'),
    path('search/', views.search_products, name='search_products'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('checkout/', views.checkout_view, name='checkout_page')
]

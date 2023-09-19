from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name="add_to_cart"),
    path('decrement_cart_item_quantity/<int:product_id>/<int:cart_item_id>', views.decrement_cart_item_quantity, name="decrement_cart_item_quantity"),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>', views.remove_cart_item, name="remove_cart_item"),
    path('checkout', views.checkout, name="checkout"),
]


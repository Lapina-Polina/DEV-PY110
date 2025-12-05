from django.urls import path, include
from .views import product_view_json, shop_view, product_page_view, \
    cart_view_json, cart_add_view_json, cart_del_view_json, cart_view, \
    coupon_check_view, delivery_estimate_view, cart_buy_now_view, cart_remove_view

app_name = 'app_store'

urlpatterns = [
    path('', shop_view, name="shop_view"),
    path('product/', product_view_json, name='product_view_json'),  # JSON список товаров или один товар по id
    path('product/<slug:page>.html', product_page_view, name='product_page_view'),  # Страница товара по slug
    path('product/<int:page>', product_page_view, name='product_page_view_by_id'),  # Страница товара по id
    path('cart/json/', cart_view_json, name='cart_view_json'),  # Корзина
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<id_product>', cart_add_view_json, name='cart_add_view_json'),
    path('cart/del/<id_product>', cart_del_view_json, name='cart_del_view_json'),
    path('coupon/check/<slug:name_coupon>/', coupon_check_view, name='coupon_check'),
    path('delivery/estimate/', delivery_estimate_view, name='delivery_estimate'),
    path('cart/buy/<str:id_product>', cart_buy_now_view, name="buy_now"),
    path('cart/remove/<str:id_product>', cart_remove_view, name="remove_now"),
]

from django.urls import path
from .views import product_view_json, shop_view, product_page_view,\
    cart_view_json, cart_add_view_json, cart_del_view_json


urlpatterns = [
    path('', shop_view),  # Главная страница
    path('product/', product_view_json),  # JSON список товаров или один товар по id
    path('product/<slug:page>.html', product_page_view),  # Страница товара по slug
    path('product/<int:page>', product_page_view),  # Страница товара по id
    path('cart/json/', cart_view_json),  # Корзина
    path('cart/add/<id_product>', cart_add_view_json),
    path('cart/del/<id_product>', cart_del_view_json),
]

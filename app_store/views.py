from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import DATABASE
from logic.services import filtering_category
from logic.control_cart import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


def product_view_json(request):
    if request.method == "GET":
        id_ = request.GET.get('id')
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE[id_], json_dumps_params={'ensure_ascii': False, 'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        category_key = request.GET.get("category")
        ordering_key = request.GET.get("ordering")
        reverse = request.GET.get("reverse", "false").lower() == "true"

        if category_key:
            data = filtering_category(DATABASE, category_key, ordering_key, reverse)
        elif ordering_key:
            data = filtering_category(DATABASE, ordering_key=ordering_key, reverse=reverse)
        else:
            data = list(DATABASE.values())

        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def shop_view(request):
    if request.method == "GET":
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'app_store/shop.html',
                      context={"products": data,
                               "category": category_key})


def product_page_view(request, page):
    if request.method == "GET":
        # Ищем текущий товар
        product = None
        for data in DATABASE.values():
            if data['html'] == page:
                product = data
                break

        if not product:
            return HttpResponse(status=404)

        # Находим товары той же категории
        category = product["category"]

        other_products = [
            p for p in DATABASE.values()
            if p["category"] == category and p["html"] != page
        ][:4]

        return render(
            request,
            "app_store/product.html",
            context={
                "product": product,
                "other_products": other_products,
            }
        )


@login_required(login_url='app_login:login_view')
def cart_view_json(request):
    username = get_user(request).username
    data = view_in_cart(username)
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})


@login_required(login_url='app_login:login_view')
def cart_add_view_json(request, id_product):
    username = get_user(request).username
    result = add_to_cart(id_product, username)
    if result:
        return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                            json_dumps_params={'ensure_ascii': False})
    return JsonResponse({"answer": "Неудачное добавление в корзину"},
                        status=404, json_dumps_params={'ensure_ascii': False})


@login_required(login_url='app_login:login_view')
def cart_del_view_json(request, id_product):
    username = get_user(request).username
    result = remove_from_cart(id_product, username)
    if result:
        return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                            json_dumps_params={'ensure_ascii': False})
    return JsonResponse({"answer": "Неудачное удаление из корзины"},
                        status=404, json_dumps_params={'ensure_ascii': False})


@login_required(login_url='app_login:login_view')
def cart_view(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_cart(username)[username]

        products = []
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id].copy()
            product["quantity"] = quantity
            product["price_total"] = "{:.2f}".format(quantity * product["price_after"])
            product["url"] = f'app_store/images/{product["url"].split("/")[-1]}'
            if product["price_after"] < product["price_before"]:
                product["discount"] = int((product["price_before"] - product["price_after"]) / product["price_before"] * 100)
            else:
                product["discount"] = None
            products.append(product)

        return render(request, "app_store/cart.html", context={"products": products})


@login_required(login_url='app_login:login_view')
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_cart(id_product, username)
        if result:
            return redirect("app_store:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")


@login_required(login_url='app_login:login_view')
def cart_remove_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        # Вызов функции удаления из корзины
        result = remove_from_cart(id_product, username)
        if result:
            # Перенаправляем пользователя обратно в корзину
            return redirect("app_store:cart_view")

        return HttpResponseNotFound("Неудачное удаление из корзины")


def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов
    DATA_COUPON = {
        "coupon": {
            "discount": 10,
            "is_valid": True
        },
        "coupon_old": {
            "discount": 20,
            "is_valid": False
        },
    }

    if request.method == "GET":
        # Проверяем, есть ли купон в базе
        coupon = DATA_COUPON.get(name_coupon)
        if coupon:
            # Если купон найден, возвращаем JSON с информацией о скидке и действительности
            return JsonResponse({
                "discount": coupon["discount"],
                "is_valid": coupon["is_valid"]
            })
        else:
            # Если купон не найден, возвращаем 404
            return HttpResponseNotFound("Неверный купон")


def delivery_estimate_view(request):
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 90},
            "Санкт-Петербург": {"price": 78},
            "fix_price": 100,  # для всех остальных городов России
        },
    }

    if request.method == "GET":
        country = request.GET.get('country')
        city = request.GET.get('city')

        if not country:
            return HttpResponseNotFound("Неверные данные")

        country_data = DATA_PRICE.get(country)
        if not country_data:
            return HttpResponseNotFound("Неверные данные")

        # Если город есть в базе — возвращаем цену
        if city in country_data:
            return JsonResponse({"price": country_data[city]["price"]})
        # Если города нет в базе, но есть fix_price — возвращаем фиксированную цену
        elif "fix_price" in country_data:
            return JsonResponse({"price": country_data["fix_price"]})
        else:
            return HttpResponseNotFound("Неверные данные")
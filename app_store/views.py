from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category
from logic.control_cart import view_in_cart, add_to_cart, remove_from_cart


def product_view_json(request):
    if request.method == "GET":
        # Обработка id из параметров запроса
        id_ = request.GET.get('id')
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE[id_], json_dumps_params={'ensure_ascii': False,
                                                                      'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации по категории и сортировке
        category_key = request.GET.get("category")  # Категория (если есть)
        ordering_key = request.GET.get("ordering")  # Ключ сортировки (если есть)
        reverse = request.GET.get("reverse", "false").lower() == "true"  # True или False

        if category_key:
            # Если указана категория и сортировка
            data = filtering_category(DATABASE, category_key=category_key,
                                      ordering_key=ordering_key,
                                      reverse=reverse)
        else:
            # Если категория не указана, но есть сортировка
            if ordering_key:
                data = filtering_category(DATABASE, ordering_key=ordering_key, reverse=reverse)
            else:
                # Если нет ни категории, ни сортировки — возвращаем все товары
                data = list(DATABASE.values())

        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


def shop_view(request):
    try:
        with open('app_store/shop.html', encoding='utf-8') as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        return HttpResponseNotFound("Страница магазина не найдена")


def product_page_view(request, page):
    # Пытаемся интерпретировать page как id
    try:
        page_id = int(page)
        product = DATABASE.get(str(page_id))
        if product:
            html_file = f'app_store/product/{product["html"]}.html'
            try:
                with open(html_file, encoding='utf-8') as f:
                    return HttpResponse(f.read())
            except FileNotFoundError:
                return HttpResponseNotFound("HTML страницы товара нет")
        return HttpResponseNotFound("Товара с таким ID нет")
    except ValueError:
        # Если page — slug
        for product in DATABASE.values():
            if product['html'] == page:
                html_file = f'app_store/product/{page}.html'
                try:
                    with open(html_file, encoding='utf-8') as f:
                        return HttpResponse(f.read())
                except FileNotFoundError:
                    return HttpResponseNotFound("HTML страницы товара нет")
        return HttpResponseNotFound("Товар с таким именем не найден")


def cart_view_json(request):
    username = ''
    data = view_in_cart(username)
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def cart_add_view_json(request, id_product):
    username = ''
    result = add_to_cart(id_product, username)
    if result:
        return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                            json_dumps_params={'ensure_ascii': False})
    return JsonResponse({"answer": "Неудачное добавление в корзину"},
                        status=404, json_dumps_params={'ensure_ascii': False})


def cart_del_view_json(request, id_product):
    username = ''
    result = remove_from_cart(id_product, username)
    if result:
        return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                            json_dumps_params={'ensure_ascii': False})
    return JsonResponse({"answer": "Неудачное удаление из корзины"},
                        status=404, json_dumps_params={'ensure_ascii': False})

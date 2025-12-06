from django.shortcuts import render, redirect
from django.http import JsonResponse
from app_store.models import DATABASE
from django.contrib.auth import get_user
from logic.control_wishlist import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from django.contrib.auth.decorators import login_required


@login_required(login_url='app_login:login_view')
def wishlist_view(request):
    username = get_user(request).username
    wishlist_data = view_in_wishlist(username).get(username, {"products": []})
    products = [DATABASE[str(pid)] for pid in wishlist_data.get("products", []) if str(pid) in DATABASE]
    return render(request, "app_wishlist/wishlist.html", context={"products": products})


@login_required(login_url='app_login:login_view')
def wishlist_view_json(request):
    username = get_user(request).username
    wishlist_data = view_in_wishlist(username).get(username, {"products": []})
    return JsonResponse(wishlist_data, json_dumps_params={"ensure_ascii": False, "indent": 4})


@login_required(login_url='app_login:login_view')
def wishlist_add_view_json(request, id_product: str):
    username = get_user(request).username
    id_product = str(id_product)

    result = add_to_wishlist(id_product, username)

    # Возвращаем 204 No Content — браузер не показывает JSON
    if result:
        return JsonResponse({"answer": "Продукт успешно добавлен в избранное"}, status=204)

    return JsonResponse({"answer": "Продукт уже в избранном или не найден"}, status=204)


@login_required(login_url='app_login:login_view')
def wishlist_del_view_json(request, id_product: str):
    username = get_user(request).username
    id_product = str(id_product)

    result = remove_from_wishlist(id_product, username)

    if result:
        return JsonResponse({"answer": "Продукт успешно удалён из избранного"}, status=204)

    return JsonResponse({"answer": "Продукт не найден в избранном"}, status=204)


@login_required(login_url='app_login:login_view')
def wishlist_remove_view(request, id_product: str):
    # Это для кнопки на странице wishlist (редирект на сам список)
    username = get_user(request).username
    id_product = str(id_product)
    result = remove_from_wishlist(id_product, username)
    if result:
        return redirect("app_wishlist:wishlist_view")
    return JsonResponse({"answer": "Неудачное удаление из избранного"}, json_dumps_params={"ensure_ascii": False})

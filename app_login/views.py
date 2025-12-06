import os
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from logic.control_cart import view_in_cart
from logic.control_wishlist import view_in_wishlist


PATH_WISHLIST = os.path.join(settings.BASE_DIR, 'wishlist.json')


def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    elif request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            # Создание/загрузка корзины
            view_in_cart(user.username)

            # Создание/загрузка избранного
            view_in_wishlist(user.username)

            return redirect('app_store:shop_view')

        return render(request, "login/login.html", context={"error": "Неверные данные"})


def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect('app_store:shop_view')
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from logic.control_cart import view_in_cart


def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    elif request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # Авторизация пользователя

            # Создание/загрузка корзины для текущего пользователя
            from django.contrib.auth import get_user
            user = get_user(request)
            view_in_cart(user.username)  # Получаем корзину, если её нет, создаем пустую

            return redirect('app_store:shop_view')  # Редирект на стартовую страницу

        # Если авторизация не удалась
        return render(request, "login/login.html", context={"error": "Неверные данные"})


def logout_view(request):
    if request.method == "GET":
        logout(request)  # Разлогиниваем пользователя
        return redirect('app_store:shop_view')  # Редирект на стартовую страницу

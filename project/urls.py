from django.contrib import admin
from django.urls import path
from random import random
from django.http import HttpResponse
from app_datetime.views import datetime_view, dynamic_datetime_view
from app_weather.views import weather_view
from app_store.views import product_view_json, shop_view


def random_view(request):
    if request.method == "GET":
        data = random()
        return HttpResponse(data)


def dynamic_random_view(request):
    if request.method == "GET":
        script = '''
            <script>
                function updateNumber() {
                    let randomNum = Math.random();
                    document.getElementById("random").innerText = randomNum; // Заменяем предыдущее значение на новое в блоке с id="random"
                }
                setInterval(updateNumber, 1000); // Запускаем обновление каждую секунду
                window.onload = updateNumber; // Генерируем первое число при загрузке
            </script>
            <body>
                <h1>Случайное число: <span id="random">Загрузка...</span></h1>
            </body>
        '''
        return HttpResponse(script)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('random/', random_view),
    path('dynamic_random/', dynamic_random_view),
    path('datetime/', datetime_view),
    path('dynamic_datetime/', dynamic_datetime_view),
    path('weather/', weather_view),
    path('product/', product_view_json),
    path('', shop_view),
]
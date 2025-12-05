from django.contrib import admin
from django.urls import path, include
from random import random
from django.http import HttpResponse
from app_datetime.views import datetime_view, dynamic_datetime_view
from app_weather.views import weather_view


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
                    document.getElementById("random").innerText = randomNum;
                }
                setInterval(updateNumber, 1000);
                window.onload = updateNumber;
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
    path('', include('app_store.urls')),
    path('login/', include('app_login.urls')),
]

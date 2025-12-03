from django.http import JsonResponse
from weather_api import current_weather


def weather_view(request):
    if request.method == "GET":
        # Вызов функции current_weather с координатами Санкт-Петербурга
        data = current_weather(lat=59.93, lon=30.31)

        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

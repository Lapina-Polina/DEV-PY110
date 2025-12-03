from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import DATABASE


def product_view_json(request):
    if request.method == "GET":
        return JsonResponse(DATABASE, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def shop_view(request):
    if request.method == "GET":
        with open('app_store/shop.html', encoding='utf-8') as f:
            data = f.read()
        return HttpResponse(data)

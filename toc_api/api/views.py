from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
import json
from .scraping import Scraping
from django.views.decorators.csrf import csrf_exempt
import time
# Create your views here.

def webscraping_all_data():
    sc = Scraping()
    sc.scrap()
    time.sleep(5)
    sc.scrap_inves()

@csrf_exempt
def go_scraping(request):
    if request.method == 'POST':
        webscraping_all_data()
        return HttpResponse("Scraping. . . . ")

@csrf_exempt
def say_hello(request):
    return HttpResponse("hello world")

@csrf_exempt
def investing(request):

    if request.method == 'POST':
        var = json.loads(request.body)["currency"]

        if var == "USD1" or var == "USD5" or var == "USD50":
            var = "USD"
        
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'data/thb-'+var.lower()+'.json')
        f = open(file_path,encoding='utf-8')
        data = json.load(f)

        return JsonResponse(data)


@csrf_exempt
def graph_(request):

    if request.method == 'POST':
        var = json.loads(request.body)["currency"]

        if var == "USD1" or var == "USD5" or var == "USD50":
            var = "USD"
        
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'data/'+str(var)+'.json')
        f = open(file_path,encoding='utf-8')
        data = json.load(f)

        return JsonResponse(data)
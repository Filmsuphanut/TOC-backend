from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
import json
# Create your views here.

def say_hello(request):
    return HttpResponse("hello world")


def investing_thb2usd(request):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'data/thb-usd.json')
    f = open(file_path)
    data = json.load(f)
    #return HttpResponse("hello world")
    return JsonResponse(data)

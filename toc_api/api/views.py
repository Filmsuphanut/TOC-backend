from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def say_hello(request):
    return HttpResponse("hello world")

# @csrf_exempt
# def investing(request):

#     if request.method == 'POST':
#         var = json.loads(request.body)["currency"]

#         if var == "USD1" or var == "USD5" or var == "USD50":
#             var = "USD"
        
#         module_dir = os.path.dirname(__file__)
#         file_path = "api/data/thb-"+var+".json"
#         f = open(file_path,encoding='utf-8')
#         data = json.load(f)

#         return JsonResponse(data)


# @csrf_exempt
# def graph_(request):

#     if request.method == 'POST':
#         var = json.loads(request.body)["currency"]

#         if var == "USD1" or var == "USD5" or var == "USD50":
#             var = "USD"
        
#         module_dir = os.path.dirname(__file__)
#         file_path = os.path.join(module_dir, 'data/'+str(var)+'.json')
#         f = open(file_path,encoding='utf-8')
#         data = json.load(f)

#         return JsonResponse(data)



###################################################################################################

@csrf_exempt
def compare(request):
    if request.method == 'POST':
        category = json.loads(request.body)["category"]
        currency = json.loads(request.body)["currency"]

    print(category,currency)
    return HttpResponse("hello world")

    var = json.loads(request.body)["currency"]
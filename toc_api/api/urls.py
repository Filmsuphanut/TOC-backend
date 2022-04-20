from django.urls import path
from . import views

urlpatterns = [
    path('say_hello/', views.say_hello),
    path('investing_thb2usd/', views.investing_thb2usd),
]
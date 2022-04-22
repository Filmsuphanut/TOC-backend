from django.urls import path
from . import views

urlpatterns = [
    path('say_hello/', views.say_hello),
    path('investing/', views.investing),
    path('graph/', views.graph_),
    #path('go_scraping/', views.go_scraping),
]
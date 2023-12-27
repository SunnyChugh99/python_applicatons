# helloapp/urls.py
from django.urls import path
from .views import hello_world, bye_django

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('bye/', bye_django, name='bye_django')
]



from django.shortcuts import render

# helloapp/views.py
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello, World!")


def bye_django(request):
    return HttpResponse("Bye, Django!")
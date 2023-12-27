from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request handler for http requests
# it contains the code for handling data, fetching, storing data

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

def say_hello(request):
    return render(request, "hello.html")


# views.py


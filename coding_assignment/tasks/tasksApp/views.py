from django.http import HttpResponse
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import render

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# def hello_world(request):
#     return render(request, 'index.html')
# def welcome_tasks_app(request):
#     return HttpResponse("Hello Peeps, Welcome to my tasks app!")


def welcome_tasks_app(request):
    return render(request, 'index.html')
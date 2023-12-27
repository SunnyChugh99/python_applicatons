from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter

# URL CONF
router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')

urlpatterns = [
    path('hello/', views.say_hello),
    path('api/', include(router.urls)),
]


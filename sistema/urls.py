from django.urls import path, include
from .views import GetPestaniaUsuario
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('sistema/pestanias/', GetPestaniaUsuario.as_view(), name="get"),
]

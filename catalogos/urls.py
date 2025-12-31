from django.urls import path, include
from .views import GeneroModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"generos", GeneroModelViewSet, basename="genero")

urlpatterns = [
    path('catalogos/', include(router.urls))
]

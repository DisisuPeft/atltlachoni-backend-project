from django.urls import path, include
from .views import GeneroModelViewSet, InstitutosView, InstitucionesModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# InstitucionesModelViewSet
router.register(r"generos", GeneroModelViewSet, basename="genero")
router.register(r"instituciones", InstitucionesModelViewSet, basename="institucion")

urlpatterns = [
    path('catalagos/genericos/instituciones/', InstitutosView.as_view(), name="get"),
    path('catalogos/', include(router.urls))
]

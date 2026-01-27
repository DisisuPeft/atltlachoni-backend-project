from django.urls import path, include
from .views import GeneroModelViewSet, InstitutosView, InstitucionesModelViewSet, NivelEducativoView, EstadosPaisView, LocalidadView, MetodoPagoView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# InstitucionesModelViewSet
router.register(r"generos", GeneroModelViewSet, basename="genero")
router.register(r"instituciones", InstitucionesModelViewSet, basename="institucion")

urlpatterns = [
    path('catalagos/genericos/instituciones/', InstitutosView.as_view(), name="get"),
    path('catalagos/genericos/niveles-educativos/', NivelEducativoView.as_view(), name="get"),
    path('catalagos/genericos/estados/', EstadosPaisView.as_view(), name="get"),
    path('catalagos/genericos/localidades/', LocalidadView.as_view(), name="get"),
    path('catalagos/genericos/metodo-pago/', MetodoPagoView.as_view(), name="get"),
    path('catalogos/', include(router.urls))
]

from django.urls import path, include
from control_escolar.views import TipoProgramaView, ModalidadesView
from rest_framework.routers import DefaultRouter
from control_escolar.controller import ProgramaEductiavoModelViewSet, EstudiantePerfilViewSet, ProgramaEducativoGenericoView, CampaniaModelViewSet

router = DefaultRouter()

router.register(r'programas-educativos', ProgramaEductiavoModelViewSet, basename="programa-educativo")
router.register(r'campanias', CampaniaModelViewSet, basename="campania")
router.register(r"estudiantes", EstudiantePerfilViewSet, basename="estudiante")

urlpatterns = [
    path('control-escolar/genericos/modalidades/', ModalidadesView.as_view(), name="get"),
    path('control-escolar/genericos/tipos-programas/', TipoProgramaView.as_view(), name="get"),
    path('control-escolar/genericos/programas/', ProgramaEducativoGenericoView.as_view(), name="get"),
    path('control-escolar/', include(router.urls))
]

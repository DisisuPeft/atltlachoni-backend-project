from django.urls import path, include
from control_escolar.views import TipoProgramaView, ModalidadesView, CampaniaView
from rest_framework.routers import DefaultRouter
from control_escolar.controller import ProgramaEductiavoModelViewSet, EstudiantePerfilViewSet, ProgramaEducativoGenericoView, CampaniaModelViewSet, TipoPagoView, InscripcionModelViewSet

router = DefaultRouter()

router.register(r'programas-educativos', ProgramaEductiavoModelViewSet, basename="programa-educativo")
router.register(r'campanias', CampaniaModelViewSet, basename="campania")
router.register(r"estudiantes", EstudiantePerfilViewSet, basename="estudiante")
router.register(r'inscripciones', InscripcionModelViewSet, basename="inscripcion")

urlpatterns = [
    path('control-escolar/genericos/modalidades/', ModalidadesView.as_view(), name="get"),
    path('control-escolar/genericos/tipos-programas/', TipoProgramaView.as_view(), name="get"),
    path('control-escolar/genericos/programas/', ProgramaEducativoGenericoView.as_view(), name="get"),
    path('control-escolar/genericos/tipo-pago/', TipoPagoView.as_view(), name="get"),
    path('control-escolar/genericos/campanias/', CampaniaView.as_view(), name="get"),
    path('control-escolar/', include(router.urls))
]

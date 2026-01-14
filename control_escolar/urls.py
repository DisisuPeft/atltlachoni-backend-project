from django.urls import path, include
from control_escolar.views import TipoProgramaView, ModalidadesView
from rest_framework.routers import DefaultRouter
from control_escolar.controller import ProgramaEductiavoModelViewSet

router = DefaultRouter()

router.register(r'programas-educativos', ProgramaEductiavoModelViewSet, basename="programa-educativo")

urlpatterns = [
    path('control-escolar/genericos/modalidades/', ModalidadesView.as_view(), name="get"),
    path('control-escolar/genericos/tipos-programas/', TipoProgramaView.as_view(), name="get"),
    path('control-escolar/', include(router.urls))
]

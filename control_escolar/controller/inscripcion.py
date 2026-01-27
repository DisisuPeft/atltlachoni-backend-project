from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from control_escolar.serializer import InscripcionSerializer
from control_escolar.models import Inscripcion
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class InscripcionModelViewSet(ModelViewSet):
    queryset = Inscripcion.objects.select_related('campania', 'estudiante').prefetch_related('pagos').all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsAutorORolPermitido]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
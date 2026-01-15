from rest_framework.viewsets import ModelViewSet
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from control_escolar.serializer import EstudiantePerfilSerializer
from user.models import EstudiantePerfil
from rest_framework.response import Response
from rest_framework import status


class EstudiantePerfilViewSet(ModelViewSet):
    queryset = EstudiantePerfil.objects.all()
    serializer_class = EstudiantePerfilSerializer
    permission_classes = [HasRoleWithRoles(['Administrador']), EsAutorORolPermitido, IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
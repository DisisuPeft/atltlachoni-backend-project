from rest_framework.viewsets import ModelViewSet
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from control_escolar.serializer import EstudiantePerfilSerializer
from user.models import EstudiantePerfil
from rest_framework.response import Response
from rest_framework import status
from control_escolar.helper import generate_matricula


class EstudiantePerfilViewSet(ModelViewSet):
    queryset = EstudiantePerfil.objects.all()
    serializer_class = EstudiantePerfilSerializer
    permission_classes = [HasRoleWithRoles(['Administrador']), EsAutorORolPermitido, IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    lookup_field = 'ref'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': "Estudiante creado con exito"}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        matricula = generate_matricula()
        serializer.save(matricula=matricula)
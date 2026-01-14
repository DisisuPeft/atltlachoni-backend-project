from rest_framework.viewsets import ModelViewSet
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from control_escolar.serializer import ProgramaEducativoSerializer
from control_escolar.models import ProgramaEducativo
from rest_framework.response import Response
from rest_framework import status


class ProgramaEductiavoModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsAutorORolPermitido]
    queryset = ProgramaEducativo.objects.select_related("modulos", "submodulos").all()
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = ProgramaEducativoSerializer
    lookup_field = 'ref'
    
    def get_queryset(self):
        search_by_name = self.request.query_params.get('search')
        
        qs = super().get_queryset()
        
        if search_by_name:
            qs = qs.filter(nombre=search_by_name)
            
        return qs
        
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response("Programa Educativo creado con exito.", status=status.HTTP_200_OK)
        
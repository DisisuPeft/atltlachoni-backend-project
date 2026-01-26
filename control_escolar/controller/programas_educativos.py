from pyexpat.errors import messages

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from control_escolar.serializer import ProgramaEducativoSerializer, ProgramaEducativoSimpleSerializer
from control_escolar.models import ProgramaEducativo
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class ProgramaEductiavoModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsAutorORolPermitido]
    queryset = ProgramaEducativo.objects.prefetch_related("modulos").all()
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = ProgramaEducativoSerializer
    lookup_field = 'ref'
    
    def get_queryset(self):
        search_by_name = self.request.query_params.get('search')
        
        qs = super().get_queryset()

        if search_by_name:
            qs = qs.filter(nombre=search_by_name)
            
        return qs
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response("Programa Educativo creado con exito.", status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)


    @action(detail=False, methods=['get'])
    def howmanyprograms(self, request):
        programas = ProgramaEducativo.objects.filter(status=1)
        if not programas:
            return Response(programas.count(), status=status.HTTP_200_OK)
        return Response(programas.count(), status=status.HTTP_200_OK)

class ProgramaEducativoGenericoView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, EsAutorORolPermitido, HasRoleWithRoles(["Administrador"])]

    def get(self, request, *args, **kwargs):
        programas = ProgramaEducativo.objects.filter(status=1)

        if not programas:
            return Response({'detail': 'No existen programas educativos'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProgramaEducativoSimpleSerializer(programas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

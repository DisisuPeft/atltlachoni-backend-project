from pyexpat.errors import messages

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from control_escolar.serializer import ProgramaEducativoSerializer, ProgramaEducativoSimpleSerializer, ModuloEducativoSerializer
from control_escolar.models import ProgramaEducativo
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from control_escolar.models import ModuloEducativo


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
        serializer = self.get_serializer(data=request.data)
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

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, HasRoleWithRoles(["Estudiante"])])
    def programa_estudiante(self, request, ref=None):
        programa = self.get_object()
        serializer = self.get_serializer(programa)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, HasRoleWithRoles(["Estudiante", "Administrador"])])
    def modulos(self, request, ref=None):
        modulo_id = request.query_params.get('modulo')
        programa = self.get_object()

        modulo = ModuloEducativo.objects.filter(programa=programa, pk=modulo_id).first()

        if not modulo:
            return Response({'detail': 'No existe el modulo'}, status=status.HTTP_404_NOT_FOUND)

        return Response(ModuloEducativoSerializer(modulo).data, status=status.HTTP_200_OK)


class ProgramaEducativoGenericoView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, EsAutorORolPermitido, HasRoleWithRoles(["Administrador"])]

    def get(self, request, *args, **kwargs):
        programas = ProgramaEducativo.objects.filter(status=1)

        if not programas:
            return Response({'detail': 'No existen programas educativos'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProgramaEducativoSimpleSerializer(programas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from catalogos.models import Genero, Institucion, NivelEducativo, EstadoPais, Localidad
from user.permission import EsAutorORolPermitido, HasRoleWithRoles
from rest_framework.permissions import IsAuthenticated
from catalogos.serializers import GeneroSerializer, InstitucionUnidadSerializer, InstitucionesSerializer, NivelEducativoSerializer, EstadoPaisSerializer, LocalidadSerializer
from user.authenticate import CustomJWTAuthentication
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class GeneroModelViewSet(ModelViewSet):
    queryset = Genero.objects.all()
    permission_classes = [IsAuthenticated, HasRoleWithRoles(['Administrador']), EsAutorORolPermitido]
    serializer_class = GeneroSerializer
    authentication_classes = [CustomJWTAuthentication]
    
    
    def get_queryset(self):
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Genero creado con exito", status=status.HTTP_200_OK)
    

class InstitucionesModelViewSet(ModelViewSet):
    queryset = Institucion.objects.all()
    permission_classes = [IsAuthenticated, HasRoleWithRoles(['Administrador']), EsAutorORolPermitido]
    serializer_class = InstitucionesSerializer
    authentication_classes = [CustomJWTAuthentication]
    
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response("Institucion creada con exito", status=status.HTTP_200_OK)
    
    
class InstitutosView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"]), EsAutorORolPermitido]
    
    def get(self, request, *args, **kwargs):
        institutos = Institucion.objects.all()
        if not institutos:
            return Response("No existen registros de institutos", status=status.HTTP_404_NOT_FOUND)
        
        serializer = InstitucionUnidadSerializer(institutos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NivelEducativoView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"]), EsAutorORolPermitido]

    def get(self, request, *args, **kwargs):
        nivel = NivelEducativo.objects.all()
        if not nivel:
            return Response("No existen registros de niveles educativos", status=status.HTTP_404_NOT_FOUND)

        serializer = NivelEducativoSerializer(nivel, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EstadosPaisView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsAutorORolPermitido]

    def get(self, request, *args, **kwargs):
        estados = EstadoPais.objects.all()
        if not estados:
            return Response("No existen estados.", status=status.HTTP_404_NOT_FOUND)
        serializer = EstadoPaisSerializer(estados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LocalidadView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsAutorORolPermitido]

    def get(self, request, *args, **kwargs):
        estado = request.query_params.get('estado')
        localidades = Localidad.objects.filter(country__id=estado).order_by('name')
        if not localidades:
            return Response("No existen localidades relacionadas a ese estado.", status=status.HTTP_404_NOT_FOUND)
        serializer = LocalidadSerializer(localidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
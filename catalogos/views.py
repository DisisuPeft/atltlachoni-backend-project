from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from catalogos.models import Genero, Institucion
from user.permission import EsAutorORolPermitido, HasRoleWithRoles
from rest_framework.permissions import IsAuthenticated
from catalogos.serializers import GeneroSerializer, InstitucionUnidadSerializer, InstitucionesSerializer
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
        
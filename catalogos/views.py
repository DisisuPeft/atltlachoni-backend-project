from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from catalogos.models import Genero
from user.permission import EsAutorORolPermitido, HasRoleWithRoles
from rest_framework.permissions import IsAuthenticated
from catalogos.serializers import GeneroSerializer
from user.authenticate import CustomJWTAuthentication
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class GeneroModelViewSet(ModelViewSet):
    queryset = Genero.objects.all()
    permission_classes = [IsAuthenticated, HasRoleWithRoles(['Administrador'])]
    serializer_class = GeneroSerializer
    authentication_classes = [CustomJWTAuthentication]
    
    
    def get_queryset(self):
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Genero creado con exito", status=status.HTTP_200_OK)
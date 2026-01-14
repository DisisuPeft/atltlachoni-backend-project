from django.shortcuts import render
from rest_framework.views import APIView
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from control_escolar.serializers import ModalidadesSimpleSerializer, TipoProgramaSimpleSerializer
from control_escolar.models import ModalidadesPrograma, TipoPrograma
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class ModalidadesView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, HasRoleWithRoles(['Administrador']), EsAutorORolPermitido]
    
    def get(self, request, *args, **kwargs):
        modalidades = ModalidadesPrograma.objects.all()
        
        if not modalidades:
            return Response("No existen modalidades para programas educativos.", status=status.HTTP_404_NOT_FOUND)
        serializer = ModalidadesSimpleSerializer(modalidades, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TipoProgramaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, HasRoleWithRoles(['Administrador']), EsAutorORolPermitido]
    
    def get(self, request, *args, **kwargs):
        tipos = TipoPrograma.objects.all()
        
        if not tipos:
            return Response("No existen tipos para clasificar el tipo de programa educativo.", status=status.HTTP_404_NOT_FOUND)
        serializer = TipoProgramaSimpleSerializer(tipos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
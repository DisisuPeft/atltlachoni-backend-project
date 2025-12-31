from django.shortcuts import render
from rest_framework.views import APIView
from user.authenticate import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from sistema.serializers import PestianiaSerializer
from user.permission import HasRoleWithRoles, HasRole
# Create your views here.


class GetPestaniaUsuario(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        modulo_uuid = request.query_params.get("ref")
        # print(modulo_uuid)
        user = request.user

        pestanias = user.pestanias_accesibles(modulo_uuid)
        
        serializer = PestianiaSerializer(pestanias, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

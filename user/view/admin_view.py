from django.shortcuts import render
from rest_framework.views import APIView
from user.authenticate import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from sistema.serializers import PestianiaSerializer
from user.permission import HasRoleWithRoles, HasRole
from user.serializers import RoleSerializer

class IsSuperUser(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, HasRole]
    
    def get(self, request):
        user = request.user
        roles = user.roles.all()
        
        serializer = RoleSerializer(roles, many=True)
        
        if not user:
            return Response("No estas autenticado para usar esta ruta.", status=status.HTTP_403_FORBIDDEN)
        
        if user.is_superuser:
            return Response({"roles": serializer.data, "superuser": True}, status=status.HTTP_200_OK)
        
        
        return Response({"roles": serializer.data, "superuser": False}, status=status.HTTP_200_OK)
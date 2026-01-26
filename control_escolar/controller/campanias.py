from rest_framework.viewsets import ModelViewSet
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from control_escolar.serializer import CampaniaSerializer
from control_escolar.models import Campania
from rest_framework.decorators import action

class CampaniaModelViewSet(ModelViewSet):
    queryset = Campania.objects.select_related('programa').all()
    serializer_class = CampaniaSerializer
    permission_classes = [IsAuthenticated, EsAutorORolPermitido, HasRoleWithRoles(['Administrador'])]
    authentication_classes = [CustomJWTAuthentication]


    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Este recurso fue creado con exito'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def howmanycampanias(self, request):
        qs = self.get_queryset()
        return Response(qs.filter(status=1).count(), status=status.HTTP_200_OK)
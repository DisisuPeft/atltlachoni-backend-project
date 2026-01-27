from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from control_escolar.serializer import TipoPagoSimpleSerializer
from control_escolar.models import TipoPago
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class TipoPagoView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsAutorORolPermitido]

    def get(self,request):
        tipo_pago = TipoPago.objects.filter(status=1)
        if not tipo_pago:
            return Response({'detail': 'No existen tipos de pago'} ,status=status.HTTP_404_NOT_FOUND)

        serializer = TipoPagoSimpleSerializer(tipo_pago, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



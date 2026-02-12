from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.authenticate import CustomJWTAuthentication
from user.permission import HasRoleWithRoles, EsAutorORolPermitido
from rest_framework.permissions import IsAuthenticated
from control_escolar.serializer import InscripcionSerializer
from control_escolar.models import Inscripcion
from rest_framework.response import Response
from rest_framework import status
from control_escolar.models import Campania
from user.models import EstudiantePerfil
from core.services import PagoService
from django.db import transaction
from rest_framework.decorators import action
from control_escolar.serializer import ModuloEducativoSerializer


class InscripcionModelViewSet(ModelViewSet):
    queryset = Inscripcion.objects.select_related('campania', 'estudiante').prefetch_related('pagos').all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsAutorORolPermitido]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        campania_id = request.query_params.get('campania')
        estudiante_uuid = request.query_params.get('estudiante')
        inscripcion_data = {}

        if not campania_id or not estudiante_uuid:
            return Response(
                {"detail": "Se requieren los parámetros del estudiante y de la campaña"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            campania = Campania.objects.get(pk=campania_id)
            estudiante = EstudiantePerfil.objects.get(ref=estudiante_uuid)

            inscripcion_data['estudiante'] = estudiante.pk
            inscripcion_data['campania'] = campania.pk

        except (Campania.DoesNotExist, EstudiantePerfil.DoesNotExist):
            return Response(
                {"detail": "Estudiante o Campaña no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.data.get('tieme_precio_custom'):
            precios = request.data.get('tieme_precio_custom', {})
            inscripcion_data.update({
                'tiene_precio_custom': True,
                'costo_inscripcion_acordado': precios.get('costo_inscripcion'),
                'costo_mensualidad_acordado': precios.get('costo_mensualidad'),
                'costo_documentacion_acordado': precios.get('costo_documentacion'),
                'notas_precio_custom': request.data.get('razon_precio_custom')
            })

        serializer = self.get_serializer(data=inscripcion_data)
        serializer.is_valid(raise_exception=True)

        inscripcion = serializer.save()

        duracion_meses = inscripcion.campania.programa.duracion_meses
        if duracion_meses is None:
            inscripcion.hard_delete()
            return Response(
                {"detail": "Duración de meses no encontrada. Debes definir primero la duración del programa"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pago_service = PagoService(inscripcion)

        result = pago_service.procesar_pago_inicial(
            monto=request.data.get('monto'),
            notas=request.data.get('notas'),
            conceptos_ids=request.data.get('tipo_pago'),
        )

        if not result['success']:
            # print(f"Borrando inscripción {inscripcion.id}")
            inscripcion.hard_delete()
            # print(f"¿Existe aún? {Inscripcion.objects.filter(id=inscripcion.id).exists()}")
            return Response(
                {"detail": result["message"]},
                status=status.HTTP_400_BAD_REQUEST
            )


        return Response({'message': result['message']}, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, HasRoleWithRoles(["Estudiante"])])
    def inscription_details_alumno(self, request):
        estudiante = request.user.user_estudianteperfil_user.first()
        estudiante_inscripcion = Inscripcion.objects.filter(estudiante=estudiante.pk)
        response = {}
        if estudiante_inscripcion is None:
            return Response({'detail': 'No esta inscrito a ningun curso'}, status=status.HTTP_400_BAD_REQUEST)
        print(estudiante_inscripcion)
        response.update( {
            'countCursos': Inscripcion.objects.filter(estudiante=estudiante.pk).count(),
            'programasInscritos': [
                {
                    'ref': i.campania.programa.ref,
                    'nombre': i.campania.programa.nombre,
                    'tipo': i.campania.programa.tipo.nombre,
                    'banner_url': i.campania.programa.banner_url,
                    'imagen_url': i.campania.programa.imagen_url,
                    'duracion': i.campania.programa.duracion_meses,
                    'modulos': ModuloEducativoSerializer(i.campania.programa.modulos, many=True).data,
                } for i in estudiante_inscripcion
            ]
        })

        return Response(response, status=status.HTTP_200_OK)
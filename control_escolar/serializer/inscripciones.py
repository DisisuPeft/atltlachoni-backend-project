from rest_framework import serializers
from control_escolar.models import Inscripcion
from django.db import transaction

class InscripcionSerializer(serializers.ModelSerializer):
    pagos = serializers.SerializerMethodField()
    estudiante_obj = serializers.SerializerMethodField()
    campania_obj = serializers.SerializerMethodField()

    # Campos para precios personalizados (opcionales)
    tiene_precio_custom = serializers.BooleanField(required=False, default=False)
    costo_inscripcion_acordado = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True
    )
    costo_mensualidad_acordado = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True
    )
    costo_documentacion_acordado = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True
    )
    notas_precio_custom = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    class Meta:
        model = Inscripcion
        fields = (
            'id', 'fecha_inscripcion', 'estudiante', 'campania_programa',
            'pagos', 'estudiante_r', 'campania_programa_r',
            'tiene_precio_custom', 'costo_inscripcion_acordado',
            'costo_mensualidad_acordado', 'costo_documentacion_acordado',
            'notas_precio_custom', 'notas_precio_custom'
        )
        read_only_fields = [
            "pagos",
            'estudiante_r', 'campania_r'
        ]

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)

    def get_pagos(self, obj):
        from control_escolar.serializer import PagoSerializer
        return PagoSerializer(obj.pagos.all(), many=True).data
    #
    def get_estudiante_obj(self, obj):
        from control_escolar.serializer import EstudiantePerfilSerializer
        estudiante = getattr(obj, "estudiante", None)
        if estudiante is None:
            return None
        return EstudiantePerfilSerializer(estudiante, many=False).data
    #
    def get_campania_obj(self, obj):
        from control_escolar.serializer import CampaniaSerializer
        c = getattr(obj, "campania_programa", None)
        if not c:
            return None
        return CampaniaSerializer(c, many=False).data
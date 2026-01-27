from rest_framework import serializers
from control_escolar.models import TipoPago, Pago

class TipoPagoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = ("id", "nombre")


class PagoSerializer(serializers.ModelSerializer):
    tipo_pago_r = serializers.CharField(source='tipo_pago', read_only=True)
    metodo_pago_r = serializers.CharField(source='metodo_pago.nombre', read_only=True)

    class Meta:
        model = Pago
        fields = (
            'id', 'inscripcion', 'tipo_pago', 'tipo_pago_r',
            'monto', 'fecha_pago', 'fecha_vencimiento', 'estado',
            'metodo_pago', "metodo_pago_r", 'referencia', 'comprobante',
            'periodo', 'numero_pago', 'notas', 'concepto'
        )
        read_only_fields = ('fecha_pago',)
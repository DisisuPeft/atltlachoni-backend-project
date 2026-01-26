from rest_framework import serializers
from control_escolar.models import Campania
from sistema.models import Empresa


class CampaniaSerializer(serializers.ModelSerializer):
    programa_nombre = serializers.SerializerMethodField()
    institucion_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Campania
        fields = ('nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'programa', 'costo_asignado', 'empresa', 'instituto', 'status', 'programa_nombre', 'institucion_nombre')
        extra_kwargs = {
            'programa': {'write_only': True},
            'institucion': {'write_only': True},
            'status': {'write_only': True},
            'empresa': {'write_only': True},
            'programa_nombre': {'read_only': True},
            'institucion_nombre': {'read_only': True},
        }



    def create(self, validated_data):
        if not validated_data['programa']:
            raise serializers.ValidationError({'detail': 'Programa no proporcionado'})

        if validated_data['fecha_inicio'] > validated_data['fecha_fin']:
            raise serializers.ValidationError({'detail': 'La fecha de inicio no puede ser mayor a la fecha final'})

        if validated_data['fecha_fin'] < validated_data['fecha_inicio']:
            raise serializers.ValidationError({'detail': 'La fecha fin no puede ser menor a la fecha de inicio'})

        empresa = Empresa.objects.get(slug='CINFA')
        if not empresa:
            raise serializers.ValidationError({'detail': 'Se debe definir una empresa'})


        return Campania.objects.create(empresa=empresa, **validated_data)


    def get_programa_nombre(self, obj):
        return obj.programa.nombre if obj.programa else None
    def get_institucion_nombre(self, obj):
        return obj.instituto.nombre if obj.instituto else None
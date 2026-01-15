from rest_framework import serializers
from catalogos.models import Genero, Institucion, NivelEducativo, EstadoPais, Localidad


class GeneroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genero
        fields = ("id", "nombre")
        
    def create(self, validated_data):
        return super().create(validated_data)
    
    
class InstitucionUnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ("id", "nombre")
        
class InstitucionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ("id", "nombre", "empresa")
        
    def create(self, validated_data):
        empresa = validated_data.pop("empresa")
        instituciones = Institucion.objects.create(empresa=empresa, **validated_data)
        return instituciones


class NivelEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelEducativo
        fields = ("id", "nombre")

        def create(self, validated_data):
            nivel = NivelEducativo.objects.create(**validated_data)
            return nivel


class EstadoPaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPais
        fields = ("id", "name")

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ("id", "name")
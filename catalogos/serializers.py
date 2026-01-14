from rest_framework import serializers
from catalogos.models import Genero, Institucion

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
        fields = ("id", "nombre")
        
    def create(self, validated_data):
        instituciones = Institucion.objects.create(**validated_data)
        return instituciones
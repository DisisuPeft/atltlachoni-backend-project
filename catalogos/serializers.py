from rest_framework import serializers
from catalogos.models import Genero

class GeneroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genero
        fields = ("id", "nombre")
        
    def create(self, validated_data):
        return super().create(validated_data)
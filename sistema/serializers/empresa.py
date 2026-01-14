from rest_framework import serializers
from sistema.models import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ("id", "slug")
    
    
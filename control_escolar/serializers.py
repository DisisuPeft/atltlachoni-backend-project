from rest_framework import serializers
from control_escolar.models import ModalidadesPrograma, TipoPrograma

class ModalidadesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModalidadesPrograma
        fields = ("id", "name")
        
    
class TipoProgramaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPrograma
        fields = ("id", "nombre")
from rest_framework import serializers
from sistema.models import Pestania, Modulo

class PestianiaSerializer(serializers.ModelSerializer):
    # modulo = ModulosSerializer()
    class Meta:
        model = Pestania
        fields = ("uuid", 'nombre', 'href', 'icon') 

class ModulosSerializer(serializers.ModelSerializer):
    # pestanias = PestianiaSerializer(many=True)
    class Meta:
        model = Modulo
        fields = ('uuid','href', 'bgColor', 'icon','nombre') 


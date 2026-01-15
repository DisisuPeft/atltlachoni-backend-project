from rest_framework import serializers
from user.models import EstudiantePerfil
from user.serializers import UserSerializer

class EstudiantePerfilSerializer(serializers.ModelSerializer):
    user_obj = UserSerializer(read_only=True)
    niv_educativo = serializers.SerializerMethodField()
    institucion_obj = serializers.SerializerMethodField()
    estado_nombre = serializers.SerializerMethodField()
    ciudad_nombre = serializers.SerializerMethodField()

    class Meta:
        model = EstudiantePerfil
        fields = ('ref', 'user_obj', 'user', 'especialidad', 'matricula', 'fecha_ingreso', 'niv_educativo', 'nivel_educativo', 'institucion', 'institucion_obj', 'estado_nombre', 'ciudad_nombre', 'estado_pais', 'cuidad')

    # def create(self, validated_data):
    #     user = validated_data.pop('user')
    #
    #     estudiante_perfil = EstudiantePerfil.objects.create(**validated_data)

    def get_niv_educativo(self, obj):
        return obj.nivel_educativo.nombre if obj.nivel_educativo else None
    def get_institucion_obj(self, obj):
        return obj.institucion.nombre if obj.institucion else None
    def get_estado_nombre(self, obj):
        return obj.estado.nombre if obj.estado.nombre else None

from rest_framework import serializers

from catalogos.models import Genero
from user.models import EstudiantePerfil, Role, UserCustomize
from user.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction

class EstudiantePerfilSerializer(serializers.ModelSerializer):
    user = serializers.DictField(write_only=True)
    nivel_educativo_nombre = serializers.SerializerMethodField()
    institucion_nombre = serializers.SerializerMethodField()
    estado_pais_nombre = serializers.SerializerMethodField()
    ciudad_nombre = serializers.SerializerMethodField()
    user_nombre = serializers.SerializerMethodField()
    user_genero = serializers.SerializerMethodField()
    user_obj = serializers.SerializerMethodField()

    class Meta:
        model = EstudiantePerfil
        fields = ('ref', 'user', 'user_obj','especialidad', 'matricula', 'fecha_ingreso', 'nivel_educativo', 'institucion', 'estado_pais', 'ciudad', 'status', 'nivel_educativo_nombre', 'institucion_nombre', 'estado_pais_nombre', 'ciudad_nombre', 'user_nombre', 'user_genero')

    @transaction.atomic
    def create(self, validated_data):
        user_rq = validated_data.pop('user')
        genero_id = user_rq.pop('genero')
        role = Role.objects.filter(nombre="Estudiante").first()
        print(role)
        if user_rq is not None:
            email = user_rq.get('email')
            if not email:
                raise serializers.ValidationError('El email es obligatorio')

            query_user = UserCustomize.objects.filter(email=email).first()
            if query_user:
                q_estudiante = EstudiantePerfil.objects.filter(user=query_user).exists()
                if not q_estudiante:
                    estudiante = EstudiantePerfil.objects.create(user=query_user, **validated_data)
                    return estudiante
                else:
                    raise serializers.ValidationError('El estudiante ya existe')
            else:
                if not role:
                    raise serializers.ValidationError('El rol no existe')
                genero = Genero.objects.get(pk=genero_id)
                if not genero:
                    raise serializers.ValidationError('El genero no existe')
                user = UserCustomize.objects.create(genero=genero, **user_rq)
                user.roles.set([role])
                estudiante = EstudiantePerfil.objects.create(user=user, **validated_data)
                return estudiante

        else:
            raise serializers.ValidationError('El perfil del estudiante debe ser definido.')


    def get_nivel_educativo_nombre(self, obj):
        return obj.nivel_educativo.nombre if obj.nivel_educativo else None

    def get_institucion_nombre(self, obj):
        return obj.institucion.nombre if obj.institucion else None

    def get_estado_pais_nombre(self, obj):
        return obj.estado_pais.name if obj.estado_pais else None

    def get_ciudad_nombre(self, obj):
        return obj.ciudad.name if obj.ciudad else None

    def get_user_nombre(self, obj):
        return f"{obj.user.nombre} {obj.user.apellido_paterno} {obj.user.apellido_materno}" if obj.user else None

    def get_user_genero(self, obj):
        return obj.user.genero.nombre if obj.user else None

    def get_user_obj(self, obj):
        from user.serializers import UserSimpleSerializer
        user = obj.user
        if user:
            return UserSimpleSerializer(user).data
        else:
            return None

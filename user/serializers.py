from user.models import UserCustomize as User
from user.models import Role
from rest_framework import serializers
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions
from catalogos.models import Genero
from rest_framework.validators import ValidationError
from django.shortcuts import get_object_or_404

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        user = authenticate(**credentials)
        if user: 
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User is deactivated')


class MeSerializer(serializers.ModelSerializer):
    modulos_accesibles = serializers.SerializerMethodField()
    # pestanias_accesibles = serializers.SerializerMethodField()
    nombre_completo = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("uuid","email", 'nombre_completo', 'modulos_accesibles')
        
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}" if obj.nombre and obj.apellido_paterno and obj.apellido_materno else ""
        
    def get_modulos_accesibles(self, obj):
        from sistema.serializers import ModulosSerializer
        
        data = obj.modulos_accesibles()

        return ModulosSerializer(data, many=True).data

    # def get_pestanias_accesibles(self, obj):
    #     from sistema.serializers import PestianiaSerializer
        
    #     data = obj.pestanias_accesibles()

    #     return PestianiaSerializer(data, many=True).data



class UserSerializer(serializers.ModelSerializer):
    genero_name = serializers.SerializerMethodField()
    roles_list = serializers.SerializerMethodField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance is None:
            self.fields['password'].required = True
        else:
            self.fields['password'].required = False    
            self.fields['password'].allow_blank = False
    
    class Meta:
        model = User
        fields = ("uuid", "nombre", "apellido_paterno", "apellido_materno", "genero",  "genero_name", "edad", "fecha_nacimiento", "telefono", "email", "status", "password", "roles_list", "roles")
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        roles = validated_data.pop("roles", [])
        password = validated_data.pop('password', None)

        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        if not roles:
            raise ValidationError("Se debe proporcionar un rol al usuario.")
        
        user.roles.set(roles)
        
        user.save()
        
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        roles_list = validated_data.pop("roles", [])
        # print(validated_data, password)
        ins = super().update(instance, validated_data)
        
        if password and len(password) > 6 and password is not None:
           ins.set_password(password)
        
        ins.roles.clear()
        ins.roles.set(roles_list)
        ins.save()
        return ins
        
    
    def get_genero_name(self, obj):
        return obj.genero.nombre if obj.genero else None
    def get_roles_list(self, obj):
        from user.serializers import RoleSerializer
        if obj.roles:
            return RoleSerializer(obj.roles, many=True).data
        return None 
    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "nombre")
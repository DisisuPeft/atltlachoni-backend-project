from rest_framework import serializers
from control_escolar.models import SubModuloEducativo, ModuloEducativo, ProgramaEducativo
from user.models import MaestroPerfil
from django.db import transaction

class SubModuloEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubModuloEducativo
        fields = [
            "id",
            "titulo",
            "descripcion",
            "orden",
            "path_class",
        ]
        
class ModuloEducativoSerializer(serializers.ModelSerializer):
    submodulos = SubModuloEducativoSerializer(many=True)

    class Meta:
        model = ModuloEducativo
        fields = [
            "id",
            "nombre",
            "horas_teoricas",
            "horas_practicas",
            "horas_totales",
            "creditos",
            "submodulos",
        ]
    @transaction.atomic
    def create(self, validated_data):
        submodulos_data = validated_data.pop("submodulos", [])
        modulo = ModuloEducativo.objects.create(**validated_data)

        for submodulo_data in submodulos_data:
            SubModuloEducativo.objects.create(
                modulo=modulo,
                **submodulo_data
            )

        return modulo
    @transaction.atomic
    def update(self, instance, validated_data):
        submodulos_data = validated_data.pop("submodulos", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Estrategia simple: borrar y recrear
        instance.submodulos.all().delete()

        for submodulo_data in submodulos_data:
            SubModuloEducativo.objects.create(
                modulo=instance,
                **submodulo_data
            )

        return instance
    
class ProgramaEducativoSerializer(serializers.ModelSerializer):
    modulos = ModuloEducativoSerializer(many=True)
    instructor = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=MaestroPerfil.objects.all()
    )

    class Meta:
        model = ProgramaEducativo
        fields = [
            "id",
            "ref",
            "nombre",
            "descripcion",
            "tipo",
            "institucion",
            "duracion_horas",
            "fecha_inicio",
            "fecha_fin",
            "duracion_meses",
            "horario",
            "costo_inscripcion",
            "costo_mensualidad",
            "costo_documentacion",
            "instructor",
            "modalidad",
            "imagen_url",
            "banner_url",
            "modulos",
        ]
        read_only_fields = ["ref"]
    @transaction.atomic
    def create(self, validated_data):
        modulos_data = validated_data.pop("modulos", [])
        instructores = validated_data.pop("instructor", [])

        programa = ProgramaEducativo.objects.create(**validated_data)

        if instructores:
            programa.instructor.set(instructores)

        for modulo_data in modulos_data:
            submodulos_data = modulo_data.pop("submodulos", [])
            modulo = ModuloEducativo.objects.create(
                programa=programa,
                **modulo_data
            )

            for submodulo_data in submodulos_data:
                SubModuloEducativo.objects.create(
                    modulo=modulo,
                    **submodulo_data
                )

        return programa
    
    @transaction.atomic
    def update(self, instance, validated_data):
        modulos_data = validated_data.pop("modulos", [])
        instructores = validated_data.pop("instructor", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if instructores is not None:
            instance.instructor.set(instructores)


        instance.modulos.all().delete()

        for modulo_data in modulos_data:
            submodulos_data = modulo_data.pop("submodulos", [])
            modulo = ModuloEducativo.objects.create(
                programa=instance,
                **modulo_data
            )

            for submodulo_data in submodulos_data:
                SubModuloEducativo.objects.create(
                    modulo=modulo,
                    **submodulo_data
                )

        return instance
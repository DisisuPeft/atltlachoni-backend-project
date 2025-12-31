from django.db import models
from common.models import Base, SoftDeleteModel, OwnerBaseModel


class Examenes(Base, SoftDeleteModel, OwnerBaseModel):
    name = models.CharField(max_length=100)
    programa_educativo = models.ForeignKey("control_escolar.ProgramaEducativo", on_delete=models.CASCADE, related_name="programa_educativo_examen")
    tipo_examen = models.ForeignKey("control_escolar.TiposExamen", on_delete=models.CASCADE, related_name="examen")
    fecha = models.DateField()

class CalificacionExamen(Base, SoftDeleteModel, OwnerBaseModel):
    estudiante = models.ForeignKey("user.UserCustomize", on_delete=models.CASCADE, related_name="estudiante_examen_calificacion")
    examen = models.ForeignKey(Examenes, on_delete=models.CASCADE, related_name="estudiante_calificacion", null=True, blank=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)


class OpcionesRespuestas(Base, SoftDeleteModel, OwnerBaseModel):
    pregunta = models.ForeignKey("control_escolar.Preguntas", on_delete=models.CASCADE, related_name="respuesta")
    text = models.TextField()
    is_correct = models.IntegerField()

class Preguntas(Base, SoftDeleteModel, OwnerBaseModel):
    examen = models.ForeignKey(Examenes, on_delete=models.CASCADE, related_name="preguntas_examen")
    enunciado = models.TextField()
    tipo = models.ForeignKey("control_escolar.TipoPreguntas", on_delete=models.CASCADE, related_name="preguntas")

class RespuestasEstudiantes(Base, SoftDeleteModel, OwnerBaseModel):
    estudiante = models.ForeignKey("user.UserCustomize", on_delete=models.CASCADE, related_name="estudiante_respuesta")
    pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE, related_name="respuesta_estudiante")
    respuesta = models.TextField()
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)

class TiposExamen(Base, SoftDeleteModel, OwnerBaseModel):
    name = models.CharField(max_length=50)


class TipoPreguntas(Base, SoftDeleteModel, OwnerBaseModel):
    name = models.CharField(max_length=50)
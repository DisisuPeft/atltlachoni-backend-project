from django.db import models
from common.models import Base, SoftDeleteModel, OwnerBaseModel


class Calificaciones(Base, SoftDeleteModel, OwnerBaseModel):
    estudiante = models.ForeignKey("user.UserCustomize", on_delete=models.CASCADE, related_name="estudiante_calificacion")
    programa_educativo = models.ForeignKey("control_escolar.ProgramaEducativo", on_delete=models.CASCADE, related_name="programa_educativo_calificacion")
    periodo = models.ForeignKey("control_escolar.Campania", on_delete=models.CASCADE, related_name="periodo_calificacion")
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    aprobado = models.BooleanField(default=False)
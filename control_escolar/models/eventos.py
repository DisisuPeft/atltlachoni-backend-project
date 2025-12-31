# from common.models import BaseCRM
from django.db import models
from common.models import Base, SoftDeleteModel, OwnerBaseModel


class TipoEvento(Base, SoftDeleteModel, OwnerBaseModel):
    nombre = models.CharField(max_length=50)
    
class Evento(Base, SoftDeleteModel, OwnerBaseModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    campania = models.ForeignKey("control_escolar.Campania", on_delete=models.CASCADE, null=True, blank=True, related_name="eventos")
    empresa = models.ForeignKey("sistema.Empresa", on_delete=models.CASCADE, null=True, blank=True, related_name="eventos")
    instituto = models.ForeignKey("catalogos.Institucion", on_delete=models.CASCADE, null=True, blank=True, related_name="eventos")
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    modalidad = models.ForeignKey("control_escolar.ModalidadesPrograma", on_delete=models.SET_NULL, related_name="evento", null=True, blank=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name="evento")
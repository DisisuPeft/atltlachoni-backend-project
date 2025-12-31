from django.db import models
from common.models import Base, SoftDeleteModel

class MetodoPago(Base, SoftDeleteModel):
    nombre = models.CharField(max_length=50, unique=True, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Métodos de Pago"
    
    def __str__(self):
        return self.nombre
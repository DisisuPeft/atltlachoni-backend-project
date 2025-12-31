from django.db import models
from common.models import Base, SoftDeleteModel, OwnerBaseModel


class TipoPago(Base):
    
    nombre = models.CharField(max_length=50, unique=True, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Tipos de Pago"
    
    def __str__(self):
        return self.nombre
    
    

class Pago(Base):
    inscripcion = models.ForeignKey("control_escolar.Inscripcion", on_delete=models.CASCADE, related_name="pagos")
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.PROTECT, related_name="pagos", null=True, blank=True)
    
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    concepto = models.CharField(max_length=50, null=True, blank=True)
    
    # Estados del pago
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('excedente', 'Excedente'),
        ('parcial', 'Parcial'),
        ('vencido', 'Vencido'),
        ('cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Información adicional
    metodo_pago = models.ForeignKey('catalogos.MetodoPago', on_delete=models.SET_NULL, null=True, blank=True, related_name="pago")
    referencia = models.CharField(max_length=100, null=True, blank=True)  # Número de transacción
    comprobante = models.CharField(max_length=255, null=True, blank=True)
    
    # Para mensualidades
    periodo = models.CharField(max_length=50, null=True, blank=True)  # "Enero 2024", "Mes 1"
    numero_pago = models.IntegerField(null=True, blank=True)  # 1, 2, 3... para mensualidades
    
    notas = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha_pago']
    
    def __str__(self):
        return f"{self.inscripcion.estudiante} - {self.tipo_pago.nombre} - ${self.monto}"
from django.db import models
from common.models import BaseCRM, OwnerBaseModel, SoftDeleteModel
from core.utils.date import get_date

class Lead(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fuente = models.ForeignKey("crm.Fuentes", on_delete=models.CASCADE, related_name="leads")
    interes = models.ForeignKey("control_escolar.ProgramaEducativo", on_delete=models.CASCADE, related_name="leads_interesado", null=True, blank=True)
    etapa = models.ForeignKey("crm.Etapas", on_delete=models.CASCADE, related_name="leads_etapa")
    estatus = models.ForeignKey("crm.Estatus", on_delete=models.CASCADE, related_name="leads_estatus")
    vendedor_asignado = models.ForeignKey("user.UserCustomize", on_delete=models.CASCADE, null=True, blank=True, related_name='leads_asignados')
    campania = models.ForeignKey("control_escolar.Campania", on_delete=models.SET_NULL, null=True, blank=True, related_name="leads")
    tiempo_primera_respuesta = models.DurationField(null=True, blank=True)
    etapa_anterior = models.ForeignKey("crm.Etapas", on_delete=models.SET_NULL, null=True, blank=True, related_name="leads_previos")
    

    @property
    def was_in_touch(self):
        return self.contactos.exists()
    
    @property
    def count_was_in_touch(self):
        return self.contactos.count()

    def registrar_contacto(self):
        ContactoLead.objects.create(lead=self)

class ContactoLead(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='contactos')
    fecha_contacto = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'contacto_lead'
        ordering = ['-fecha_contacto']

class Notas(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='notas', null=True)
    texto = models.TextField()
    usuario = models.ForeignKey("user.UserCustomize", on_delete=models.SET_NULL, null=True, blank=True)


class Observaciones(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='observaciones', null=True)
    texto = models.TextField(null=True)
    usuario = models.ForeignKey("user.UserCustomize", on_delete=models.SET_NULL, null=True, blank=True)


class SeguimientoProgramado(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='seguimientos')
    fecha = models.DateField()
    descripcion = models.TextField()
    responsable = models.ForeignKey("user.UserCustomize", on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)


class HistorialLeadInstitucion(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="historial_lead_inst")
    fecha_asignacion = models.DateField(auto_now_add=True)
    cambiado_por = models.ForeignKey("user.UserCustomize", on_delete=models.SET_NULL, null=True, related_name="historial_lead_inst")



# """
# NO OLVIDAR QUE EL HISTORIAL DEBE SER ACTUALIZADO EN LA CREACION Y EN LA ACTUALIZACION DE LA ETAPA
# """
class HistorialEtapa(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='historial_etapas')
    etapa = models.ForeignKey("crm.Etapas", on_delete=models.CASCADE)
    fecha_entrada = models.DateField(auto_now_add=True)
    fecha_salida = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_entrada']


class ArchivoLead(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='archivos')
    path = models.CharField(max_length=255)
    nombre = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=True)
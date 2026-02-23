from django.db import models
from common.models import BaseCRM, BaseFileEntity
from django.conf import settings
from core.utils.file_helpers import comprobante_validacion_path

class PlanPago(BaseCRM):
    lead = models.ForeignKey("crm.Lead", on_delete=models.CASCADE, related_name='planes_pago')
    campania = models.ForeignKey('control_escolar.Campania', on_delete=models.PROTECT)

    # Montos propuestos
    inscripcion_propuesta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    mensualidad_propuesta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    num_mensualidades = models.IntegerField()
    documentacion_propuesta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Calendario de pagos
    fecha_primera_mensualidad = models.DateField()

    # Becas/Descuentos
    tiene_beca = models.BooleanField(default=False)
    tipo_beca = models.CharField(max_length=100, null=True, blank=True)
    porcentaje_descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    # Auditoría
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='planes_creados'
    )
    aprobado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planes_aprobados',
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)

    notas_vendedor = models.TextField(blank=True, null=True)


class Validacion(BaseCRM):
    plan_pago = models.ForeignKey(
        PlanPago,
        on_delete=models.CASCADE,
        related_name='validaciones'
    )

    # Comprobante
    comprobante_pago = models.ImageField(
        upload_to='validaciones/comprobantes/%Y/%m/',
    )
    monto_pagado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    fecha_pago = models.DateField()

    # Auditoría
    subido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='validaciones_subidas',
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)

    validado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='validaciones_revisadas',
    )
    fecha_validacion = models.DateTimeField(null=True, blank=True)

    # Rechazo
    motivo_rechazo = models.TextField(
        blank=True,
        null=True
    )

    notas_internas = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha_subida']
        indexes = [
            models.Index(fields=['plan_pago']),
        ]


class ComprobanteValidacion(BaseFileEntity):
    validacion = models.ForeignKey(
        'crm.Validacion',
        on_delete=models.CASCADE,
        related_name='comprobantes'
    )

    file = models.FileField(
        upload_to=comprobante_validacion_path,  # ← Función específica
        max_length=500,
        verbose_name="Comprobante"
    )

    # Validaciones específicas
    monto_visible = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    banco_origen = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    referencia = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Comprobante {self.validacion.id} - {self.original_name}"


# class DocumentoEstudiante(BaseFileEntity):
#     """
#     Documentos oficiales del estudiante (INE, CURP, títulos, etc.)
#     """
#
#     class TipoDocumento(models.TextChoices):
#         CURP = 'curp', 'CURP'
#         INE = 'ine', 'INE/IFE'
#         COMPROBANTE_DOMICILIO = 'comprobante_domicilio', 'Comprobante de Domicilio'
#         ACTA_NACIMIENTO = 'acta_nacimiento', 'Acta de Nacimiento'
#         TITULO = 'titulo', 'Título Profesional'
#         CEDULA = 'cedula', 'Cédula Profesional'
#         CERTIFICADO = 'certificado', 'Certificado de Estudios'
#         FOTO = 'foto', 'Fotografía'
#         OTRO = 'otro', 'Otro'
#
#     estudiante = models.ForeignKey(
#         'user.EstudiantePerfil',
#         on_delete=models.CASCADE,
#         related_name='documentos'
#     )
#
#     tipo_documento = models.CharField(
#         max_length=30,
#         choices=TipoDocumento.choices,
#         db_index=True,
#         verbose_name="Tipo de documento"
#     )
#
#     # Validación del documento
#     validado = models.BooleanField(
#         default=False,
#         verbose_name="¿Validado?"
#     )
#
#     validado_por = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='documentos_validados',
#         verbose_name="Validado por"
#     )
#
#     fecha_validacion = models.DateTimeField(
#         null=True,
#         blank=True,
#         verbose_name="Fecha de validación"
#     )
#
#     notas_validacion = models.TextField(
#         blank=True,
#         verbose_name="Notas de validación",
#         help_text="Razón de aprobación o rechazo"
#     )
#
#     # Vigencia (para documentos que expiran)
#     fecha_emision = models.DateField(
#         null=True,
#         blank=True,
#         verbose_name="Fecha de emisión"
#     )
#
#     fecha_vencimiento = models.DateField(
#         null=True,
#         blank=True,
#         verbose_name="Fecha de vencimiento"
#     )
#
#     class Meta:
#         db_table = 'estudiantes_documento'
#         verbose_name = 'Documento de Estudiante'
#         verbose_name_plural = 'Documentos de Estudiantes'
#         unique_together = [['estudiante', 'tipo_documento', 'status']]
#         # Solo un documento activo de cada tipo
#         indexes = [
#             models.Index(fields=['estudiante', 'tipo_documento']),
#             models.Index(fields=['validado', 'tipo_documento']),
#         ]
#
#     def __str__(self):
#         return f"{self.estudiante.user.get_full_name()} - {self.get_tipo_documento_display()}"
#
#     @property
#     def esta_vigente(self):
#         """Verificar si el documento está vigente."""
#         if not self.fecha_vencimiento:
#             return True
#         from django.utils import timezone
#         return self.fecha_vencimiento > timezone.now().date()
#
#
# # ========== ARCHIVOS DE PLAN DE PAGO ==========
# class AnexoPlanPago(BaseFileEntity):
#     """
#     Anexos adjuntos al plan de pago (contratos, propuestas firmadas, etc.)
#     """
#     plan_pago = models.ForeignKey(
#         'crm.PlanPago',
#         on_delete=models.CASCADE,
#         related_name='anexos'
#     )
#
#     TIPOS = [
#         ('propuesta', 'Propuesta Comercial'),
#         ('contrato', 'Contrato'),
#         ('convenio', 'Convenio de Pago'),
#         ('otro', 'Otro'),
#     ]
#
#     tipo_anexo = models.CharField(
#         max_length=20,
#         choices=TIPOS,
#         default='otro'
#     )
#
#     class Meta:
#         db_table = 'crm_anexo_plan_pago'
#         verbose_name = 'Anexo de Plan de Pago'
#         verbose_name_plural = 'Anexos de Planes de Pago'
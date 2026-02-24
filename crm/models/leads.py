from django.db import models
from common.models import BaseCRM, OwnerBaseModel, SoftDeleteModel, BaseFileEntity
from core.utils.date import get_date

class Lead(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    nombre_completo = models.CharField(max_length=100, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fuente = models.ForeignKey("crm.Fuentes", on_delete=models.CASCADE, related_name="leads")
    programa_objetivo = models.ForeignKey("control_escolar.ProgramaEducativo", on_delete=models.CASCADE, related_name="leads_interesado", null=True, blank=True)
    etapa = models.ForeignKey("crm.Etapas", on_delete=models.CASCADE, related_name="leads_etapa")
    estatus = models.ForeignKey("crm.Estatus", on_delete=models.CASCADE, related_name="leads_estatus")
    vendedor_asignado = models.ForeignKey("user.UserCustomize", on_delete=models.CASCADE, null=True, blank=True, related_name='leads_asignados')
    campania = models.ForeignKey("control_escolar.Campania", on_delete=models.SET_NULL, null=True, blank=True, related_name="leads")
    tiempo_primera_respuesta = models.DurationField(null=True, blank=True)
    etapa_anterior = models.ForeignKey("crm.Etapas", on_delete=models.SET_NULL, null=True, blank=True, related_name="leads_previos")


class TipoInteraccion(BaseCRM, SoftDeleteModel):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )

    codigo = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Código",
        help_text="Identificador único (ej: llamada, whatsapp, email)"
    )

    icono = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Icono/Emoji",
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )

    requiere_duracion = models.BooleanField(
        default=False,
        verbose_name="¿Requiere duración?",
        help_text="Para llamadas, reuniones, videollamadas"
    )

    requiere_telefono = models.BooleanField(
        default=False,
        verbose_name="¿Requiere número de teléfono?",
        help_text="Para WhatsApp, llamadas, SMS"
    )

    permite_archivos = models.BooleanField(
        default=True,
        verbose_name="¿Permite archivos adjuntos?"
    )

    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización en listas"
    )

    class Meta:
        verbose_name = 'Tipo de Interacción'
        verbose_name_plural = 'Tipos de Interacción'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return f"{self.icono} {self.nombre}" if self.icono else self.nombre


class EstadoInteraccion(BaseCRM, SoftDeleteModel):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )

    codigo = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Código",
        help_text="pendiente, completada, no_respondio, fallida"
    )

    color = models.CharField(
        max_length=7,
        default="#6B7280",
        verbose_name="Color (Hex)",
        help_text="Color para visualización en UI (ej: #10B981)"
    )

    es_final = models.BooleanField(
        default=True,
        verbose_name="¿Es estado final?",
        help_text="True para completada/fallida, False para pendiente"
    )

    orden = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Estado de Interacción'
        verbose_name_plural = 'Estados de Interacción'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class TipoSeguimiento(BaseCRM, SoftDeleteModel):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )

    codigo = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Código"
    )

    icono = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Icono"
    )

    # Al completar, auto-crea InteraccionLead con este tipo
    tipo_interaccion_default = models.ForeignKey(
        TipoInteraccion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tipo de interacción al completar",
        help_text="Cuando se marca como completado, se crea una interacción de este tipo"
    )

    orden = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Tipo de Seguimiento'
        verbose_name_plural = 'Tipos de Seguimiento'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return f"{self.icono} {self.nombre}" if self.icono else self.nombre


class TipoAdjunto(BaseCRM, SoftDeleteModel):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )

    codigo = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Código",
        null=True,
        blank=True
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )

    # Restricciones de archivo
    extensiones_permitidas = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Extensiones permitidas",
        help_text="Separadas por coma: jpg,png,pdf,mp3"
    )

    tamano_maximo_mb = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Tamaño máximo (MB)",
        help_text="Límite de tamaño para este tipo de archivo"
    )

    orden = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Tipo de Adjunto'
        verbose_name_plural = 'Tipos de Adjunto'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class NivelTemperatura(BaseCRM, SoftDeleteModel):
    """
    Catálogo de niveles de temperatura del lead.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )

    codigo = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Código"
    )

    icono = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Icono",
    )

    color = models.CharField(
        max_length=7,
        default="#6B7280",
        verbose_name="Color (Hex)",
        help_text="#3B82F6 (azul), #F59E0B (naranja), #EF4444 (rojo)"
    )

    puntuacion = models.IntegerField(
        default=0,
        verbose_name="Puntuación",
        help_text="Para ordenar: Frío=1, Tibio=2, Caliente=3"
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Qué significa este nivel de temperatura"
    )

    orden = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Nivel de Temperatura'
        verbose_name_plural = 'Niveles de Temperatura'
        ordering = ['puntuacion', 'orden']

    def __str__(self):
        return f"{self.icono} {self.nombre}" if self.icono else self.nombre



class InteraccionLead(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='interacciones'
    )

    tipo = models.ForeignKey(
        TipoInteraccion,
        on_delete=models.PROTECT,
        verbose_name="Tipo de interacción",
        related_name='interacciones'
    )

    estado = models.ForeignKey(
        EstadoInteraccion,
        on_delete=models.PROTECT,
        verbose_name="Estado",
        related_name='interacciones'
    )

    # Contenido
    asunto = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Asunto/Título"
    )

    contenido = models.TextField(
        verbose_name="Contenido/Notas"
    )

    # Fecha y duración
    fecha_interaccion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de interacción"
    )

    duracion_minutos = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Duración (minutos)"
    )

    # Responsable
    usuario = models.ForeignKey(
        "user.UserCustomize",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interacciones_lead',
        verbose_name="Registrado por"
    )

    # Metadata específica
    numero_telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Número de teléfono"
    )

    mensaje_enviado = models.BooleanField(
        default=False,
        verbose_name="¿Mensaje enviado?"
    )

    mensaje_recibido = models.BooleanField(
        default=False,
        verbose_name="¿Mensaje recibido?"
    )

    url_externa = models.URLField(
        blank=True,
        verbose_name="URL externa"
    )

    # Resultado
    proximo_paso = models.TextField(
        blank=True,
        verbose_name="Próximo paso acordado"
    )
    temperatura_post = models.ForeignKey(
        NivelTemperatura,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Temperatura después de la interacción",
        related_name='interacciones'
    )

    class Meta:
        verbose_name = 'Interacción con Lead'
        verbose_name_plural = 'Interacciones con Leads'
        indexes = [
            models.Index(fields=['lead', 'tipo', '-fecha_interaccion']),
            models.Index(fields=['tipo', 'estado']),
            models.Index(fields=['usuario', '-fecha_interaccion']),
        ]

    def __str__(self):
        return f"{self.tipo.nombre} - {self.lead.nombre} - {self.fecha_interaccion.strftime('%d/%m/%Y')}"

    @property
    def fue_exitosa(self):
        """Determina si la interacción fue exitosa."""
        return (self.estado.es_final and
                self.estado.codigo == 'completada' and
                (self.mensaje_recibido or self.tipo.codigo == 'nota_interna'))


class SeguimientoProgramado(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='seguimientos'
    )

    tipo = models.ForeignKey(
        TipoSeguimiento,
        on_delete=models.PROTECT,
        verbose_name="Tipo de seguimiento",
        related_name='seguimientos'
    )

    fecha_programada = models.DateTimeField(
        verbose_name="Fecha programada"
    )

    descripcion = models.TextField(
        verbose_name="Descripción/Recordatorio"
    )

    responsable = models.ForeignKey(
        "user.UserCustomize",
        on_delete=models.CASCADE,
        related_name='seguimientos_asignados'
    )

    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)

    # Cuando se completa, se crea una InteraccionLead
    interaccion_resultado = models.OneToOneField(
        InteraccionLead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='seguimiento_origen'
    )

    class Meta:
        ordering = ['fecha_programada']
        verbose_name = 'Seguimiento Programado'
        verbose_name_plural = 'Seguimientos Programados'

    def __str__(self):
        return f"{self.tipo.nombre} - {self.lead.nombre} - {self.fecha_programada.strftime('%d/%m/%Y')}"


class HistorialEtapa(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='historial_etapas')
    etapa = models.ForeignKey("crm.Etapas", on_delete=models.CASCADE)
    fecha_entrada = models.DateField(auto_now_add=True)
    fecha_salida = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha_entrada']


class ArchivoLead(BaseFileEntity):
    interaccion = models.ForeignKey(
        InteraccionLead,
        on_delete=models.CASCADE,
        related_name='archivos',
        null = True,
        blank = True
    )
    tipo_adjunto = models.ForeignKey(
        TipoAdjunto,
        on_delete=models.PROTECT,
        verbose_name="Tipo de adjunto",
        related_name='archivos',
        null=True,
        blank=True
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden"
    )


class TemperaturaLead(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    """
    Temperatura ACTUAL del lead.
    """
    lead = models.OneToOneField(
        Lead,
        on_delete=models.CASCADE,
        related_name='temperatura_actual'
    )
    temperatura = models.ForeignKey(
        NivelTemperatura,
        on_delete=models.PROTECT,
        verbose_name="Temperatura actual",
        related_name='leads_actuales'
    )

    ultima_actualizacion = models.DateTimeField(auto_now=True)

    actualizado_por = models.ForeignKey(
        "user.UserCustomize",
        on_delete=models.SET_NULL,
        null=True,
        related_name='temperaturas_actualizadas'
    )

    def __str__(self):
        return f"{self.lead.nombre} - {self.temperatura.nombre}"
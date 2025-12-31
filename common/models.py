from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.utils.date import get_today
from core.utils.date import get_formatted_short_date
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
# Create your models here.

# modelo base para registros
class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(app_label)s_%(class)s_deleted_by')

    def delete(self, using=None, keep_parents=False, user=None):
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save(update_fields=['deleted_at', 'deleted_by'])
    
    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=['deleted_at', 'deleted_by'])

    class Meta:
        abstract = True

class OwnerBaseModel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_owner', null=True, blank=True)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(app_label)s_%(class)s_edited_by')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(app_label)s_%(class)s_created_by')
    class Meta:
        abstract = True

# Modelo base para los usuario o modelos que no requieran soft delete
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=1)

    class Meta:
        abstract = True
    
    @property
    def created_at_format(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')
    
    @property
    def is_recent(self):
        return (timezone.now() - self.created_at).days < 7


class BaseFileEntity(Base):
    
    class FileType(models.TextChoices):
        DOCUMENT = 'document', 'Documento'
        IMAGE = 'image', 'Imagen'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        ARCHIVE = 'archive', 'Archivo comprimido'
        OTHER = 'other', 'Otro'
    
    
    # Nombre original del archivo
    original_name = models.CharField(
        max_length=500,
        verbose_name="Nombre original"
    )
    
    # Nombre único en almacenamiento
    storage_name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="Nombre en almacenamiento",
        help_text="Nombre único generado para evitar colisiones"
    )
    
    # Tipo MIME
    mime_type = models.CharField(
        max_length=100,
        verbose_name="Tipo MIME"
    )
    
    # Tamaño en bytes
    size = models.BigIntegerField(
        verbose_name="Tamaño (bytes)",
        help_text="Tamaño del archivo en bytes"
    )
    
    # Ruta relativa dentro del storage
    path = models.CharField(
        max_length=1000,
        verbose_name="Ruta relativa",
        help_text="Ruta relativa dentro del bucket/carpeta"
    )
    
    # Relación con usuario (agregado en Django)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_files',
        verbose_name="Subido por"
    )
    
    
    # Campos adicionales útiles
    file_type = models.CharField(
        max_length=20,
        choices=FileType.choices,
        default=FileType.OTHER,
        db_index=True,
        verbose_name="Tipo de archivo"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción opcional del archivo"
    )
    
    is_public = models.BooleanField(
        default=False,
        verbose_name="¿Es público?",
        help_text="¿Puede ser accedido sin autenticación?"
    )
    
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mime_type', 'created_at']),
            models.Index(fields=['file_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.original_name} ({self.get_file_type_display()})"
    
    @property
    def file_extension(self):
        """Obtener extensión del archivo"""
        if '.' in self.original_name:
            return self.original_name.split('.')[-1].lower()
        return ''
    
    @property
    def size_formatted(self):
        """Tamaño formateado (KB, MB, GB)"""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 ** 2:
            return f"{self.size / 1024:.1f} KB"
        elif self.size < 1024 ** 3:
            return f"{self.size / (1024 ** 2):.1f} MB"
        else:
            return f"{self.size / (1024 ** 3):.1f} GB"
    
    @property
    def full_path(self):
        """Ruta completa (path + storage_name)"""
        return os.path.join(self.path, self.storage_name)
    
    @property
    def download_url(self):
        """URL para descargar el archivo (implementar según storage)"""
        # Esto dependerá de tu configuración de almacenamiento
        # Ejemplo para S3 o almacenamiento en la nube
        return f"/api/files/{self.id}/download/"
    
    @property
    def preview_url(self):
        """URL para previsualizar (si es imagen/PDF)"""
        if self.file_type in [self.FileType.IMAGE, self.FileType.DOCUMENT]:
            return f"/api/files/{self.id}/preview/"
        return None
    
    def get_absolute_url(self):
        """URL absoluta para Django admin o vistas"""
        return f"/files/{self.id}/"
    
    def delete(self, *args, **kwargs):
        """
        Override para eliminar archivo físico al eliminar registro
        """
        from django.core.files.storage import default_storage
        try:
            # Eliminar archivo físico
            if default_storage.exists(self.full_path):
                default_storage.delete(self.full_path)
        except:
            pass  # Log error pero continuar con eliminación DB
        finally:
            super().delete(*args, **kwargs)



class BaseAcademico(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_user', null=True, blank=True)
    nivel_educativo = models.ForeignKey('catalogos.NivelEducativo', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_nivel', null=True, blank=True)
    institucion = models.ForeignKey('catalogos.Institucion', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_institucion', null=True, blank=True)
    estado_pais = models.ForeignKey("catalogos.EstadoPais", on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_estado_pais", null=True, blank=True)
    ciudad = models.ForeignKey("catalogos.Ciudad", on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_ciudad", null=True, blank=True)

    class Meta:
        abstract = True
        
class BaseCRM(Base, SoftDeleteModel):
    empresa = models.ForeignKey('sistema.Empresa', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_empresa', null=True, blank=True)
    instituto = models.ForeignKey('catalogos.Institucion', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_instituto', null=True, blank=True)

    class Meta:
        abstract = True
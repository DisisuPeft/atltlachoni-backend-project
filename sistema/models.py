from django.db import models
from common.models import Base
from django.contrib.auth.models import Permission
import uuid
# Create your models here.


class Empresa(Base):
    nombre = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=True, blank=True)  # Para usar en URLs
    logo = models.CharField(max_length=255, blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email_contacto = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    rfc = models.CharField(max_length=20, null=True, blank=True)


# NAVEGACION

# El menú NO autoriza, solo refleja.
# La seguridad vive fuera de la navegación.

"""
SEGURIDAD       → roles, permisos, ownership
NAVEGACIÓN      → módulos, pestañas
PREFERENCIA UX  → ocultar, ordenar, fijar

Cada pestaña corresponde a un permiso, no a un rol.


9. Regla de oro para no volver atrás

Si un elemento del menú requiere lógica de seguridad, eso NO es UI.

Y su complemento:

Si algo es solo visual, jamás debe decidir permisos.
"""

class Modulo(Base):
    nombre = models.CharField(max_length=50)
    icon_path = models.CharField(max_length=50, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    bgColor = models.CharField(max_length=20, null=True, blank=True)
    textColor = models.CharField(max_length=20, null=True, blank=True)
    href = models.CharField(max_length=50, null=True, blank=True)
    orden = models.IntegerField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    class Meta:
        ordering = ['orden']

class Pestania(Base):
    nombre = models.CharField(max_length=50)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name="pestanias")
    href = models.CharField(max_length=50, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    icon_path = models.CharField(max_length=50, null=True, blank=True)
    orden = models.IntegerField(null=True, blank=True)
    permission = models.ManyToManyField(Permission, related_name="pestanias", blank=True) 
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['orden']
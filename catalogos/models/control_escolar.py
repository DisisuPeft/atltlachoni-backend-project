from django.db import models
from common.models import Base
from django.conf import settings


# class EstatusAlummo(Base):
#     nombre = models.CharField(max_length=50)

class NivelEducativo(Base):
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    orden = models.IntegerField(default=0)
    
class GradoEscolar(Base):
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    orden = models.IntegerField(default=0)
    nivel_educativo = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE, related_name="grados_escolares")
    
class Institucion(Base):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email_contacto = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    responsable = models.ForeignKey("user.UserCustomize", on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.ForeignKey("sistema.Empresa", on_delete=models.CASCADE, related_name="institucion_academica")
    activa = models.IntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    unidad_usuario = models.ManyToManyField("user.UserCustomize", related_name="unidad_negocio")



class CambioDepartamento(Base):
    """
    Registra cambios de departamento de usuarios
    """
    usuario = models.ForeignKey(
        "user.UserCustomize",
        on_delete=models.CASCADE,
        related_name='cambios_departamento',
        verbose_name="Usuario"
    )
    
    departamento_anterior = models.ForeignKey(
        'catalogos.Departamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cambios_salida',
        verbose_name="Departamento anterior"
    )
    
    departamento_nuevo = models.ForeignKey(
        'catalogos.Departamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cambios_entrada',
        verbose_name="Departamento nuevo"
    )
    
    motivo = models.TextField(
        blank=True,
        verbose_name="Motivo del cambio"
    )
    
    realizado_por = models.ForeignKey(
        "user.UserCustomize",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cambios_realizados',
        verbose_name="Realizado por"
    )
    
    class Meta:
        verbose_name = "Cambio de Departamento"
        verbose_name_plural = "Cambios de Departamento"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.usuario} cambió el {self.created_at.date()}"


class Departamento(Base):
    nombre = models.CharField(max_length=80, unique=True, null=True, blank=True)
    icono = models.CharField(max_length=50, null=True, blank=True)
    jefe_departamento = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="jefe_departamento", verbose_name="Manager" 
    )
    instituto = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name="departamentos")

    def agregar_miembro(self, user, agregado_por=None):
        """
        Agrega un miembro al departamento.
        Args:
            usuario: UserCustomize a agregar
            agregado_por: Quién realiza la acción (opcional)
        """
        
        if user.departamento == self:
            return
        if user.departamento:
            CambioDepartamento.objects.create(
                usuario=user,
                departamento_anterior=user.departamento,
                departamento_nuevo=self,
                realizado_por=agregado_por,
                motivo=f"Agregado por {agregado_por}" if agregado_por else "Agregado al departamento",
            )
        user.departamento = self
        user.save(update_fields=["departamento"])

    def quitar_miembro(self, user, quitado_por=None):
        """
        Quita un miembro del departamento.
        Args:
            usuario: UserCustomize a quitar
            quitado_por: Quién realiza la acción (opcional)
        """
        if user.departamento != self:
            return
        
        CambioDepartamento.objects.create(
                usuario=user,
                departamento_anterior=self,
                departamento_nuevo=None,
                realizado_por=quitado_por,
                motivo=f"Quitado por {quitado_por}" if quitado_por else "Quitado del departamento",
        )
        user.departamento = None
        user.save(update_fields=["departamento"])


from django.db import models
from common.models import Base, OwnerBaseModel, BaseFileEntity, SoftDeleteModel

class TipoPrograma(Base, OwnerBaseModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    
    
class ModalidadesPrograma(Base, OwnerBaseModel, SoftDeleteModel):
    name = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    sincronia = models.CharField(max_length=200, blank=True, null=True) 


class ProgramaEducativo(Base, OwnerBaseModel, SoftDeleteModel):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.ForeignKey(TipoPrograma, on_delete=models.CASCADE, related_name="programas", blank=True, null=True)
    institucion = models.ForeignKey("catalogos.Institucion", on_delete=models.CASCADE, related_name="programas_por_institucion", blank=True, null=True)
    duracion_horas = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    duracion_meses = models.IntegerField(null=True, blank=True)
    horario = models.CharField(max_length=200, blank=True, null=True)  # ej. Sábados y Domingos de 8 a 14 hrs
    costo_inscripcion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_mensualidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_documentacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    instructor = models.ManyToManyField("user.MaestroPerfil", related_name="programas", blank=True)
    modalidad = models.ForeignKey(ModalidadesPrograma, on_delete=models.CASCADE, related_name="programas", null=True, blank=True)
    imagen_url = models.CharField(max_length=255, null=True, blank=True)
    banner_url = models.CharField(max_length=255, null=True, blank=True)



class Inscripcion(Base, OwnerBaseModel, SoftDeleteModel):
    estudiante = models.ForeignKey('user.EstudiantePerfil', on_delete=models.CASCADE, related_name="inscripcion")
    campania = models.ForeignKey('control_escolar.Campania', on_delete=models.CASCADE, related_name="inscripciones")
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.IntegerField(default=0) 
    costo_inscripcion_acordado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Precio acordado con el asesor para esta inscripción específica"
    )
    costo_mensualidad_acordado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    costo_documentacion_acordado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    tiene_precio_custom = models.BooleanField(
        default=False,
        help_text="Indica si esta inscripción tiene precios personalizados"
    )
    
    notas_precio_custom = models.TextField(
        blank=True, 
        null=True,
        help_text="Razón del precio personalizado (promoción, beca, acuerdo especial)"
    )


    class Meta:
        unique_together = ('estudiante', 'campania')
        
    @property
    def total_pagado(self):
        # Si existe la anotación, úsala (más eficiente)
        if hasattr(self, 'total_pagado_calc'):
            return self.total_pagado_calc
        # Fallback: calcular manualmente
        return self.pagos.filter(estado='completado').aggregate(
            total=models.Sum('monto')
        )['total'] or 0

    @property
    def saldo_pendiente(self):
        # Si existe la anotación, úsala
        if hasattr(self, 'saldo_pendiente_calc'):
            return self.saldo_pendiente_calc
        
        # Fallback: calcular con costos finales (custom o normales)
        total_requerido = (
            self.costo_inscripcion_final +  # ← Usa las properties que ya definiste
            self.costo_mensualidad_final * self.campania_programa.programa.duracion_meses +
            self.costo_documentacion_final
        )
        return total_requerido - self.total_pagado

        # Propiedades para obtener el precio real
    @property
    def costo_inscripcion_final(self):
        if self.tiene_precio_custom and self.costo_inscripcion_acordado:
            return self.costo_inscripcion_acordado
        return self.campania_programa.costo_inscripcion_real
    
    @property
    def costo_mensualidad_final(self):
        if self.tiene_precio_custom and self.costo_mensualidad_acordado:
            return self.costo_mensualidad_acordado
        return self.campania_programa.costo_mensualidad_real
    
    @property
    def costo_documentacion_final(self):
        if self.tiene_precio_custom and self.costo_documentacion_acordado:
            return self.costo_documentacion_acordado
        return self.campania_programa.costo_documentacion_real





class Dirigido(Base, OwnerBaseModel, SoftDeleteModel):
    nombre = models.TextField()

    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="dirigido")
    
class PublicoObjetivo(Base, OwnerBaseModel, SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name='publico_objetivo')
    
class PerfilIngreso(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="perfil_ingreso")
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=0)


class RequisitoActitudinal(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisitos_actitudinales")
    texto = models.CharField(max_length=300)

    
class RequisitoDeseable(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisitos_deseables")
    texto = models.CharField(max_length=300)


class EnfoquePedagogico(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="enfoque_pedagogico")
    texto = models.CharField(max_length=300)


class RequisitoIngreso(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisito_ingreso")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)

    
class RequisitoPermanencia(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisito_permanencia")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)

    
class RequisitoEgreso(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="requisito_egreso")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)


class PerfilEgreso(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="perfil_egreso")
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=0)


class ResultadoAplicacion(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="resultado_aplicacion")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)


class ResultadoActualizacion(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="resultado_actualizacion")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)


class ResultadoCrecimiento(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="resultado_crecimiento")
    texto = models.CharField(max_length=300)
    orden = models.PositiveIntegerField(default=0)


class JustificacionPrograma(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="justificacion")
    contenido = models.TextField()

    
class ModuloEducativo(Base, OwnerBaseModel, SoftDeleteModel):
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="modulos")
    nombre = models.CharField(max_length=300)
    horas_teoricas = models.IntegerField()
    horas_practicas = models.IntegerField()
    horas_totales = models.IntegerField()
    creditos = models.DecimalField(max_digits=4, decimal_places=2)
    
    
    
class CalendarioModulo(Base, OwnerBaseModel, SoftDeleteModel):
    modulo = models.ForeignKey(ModuloEducativo, on_delete=models.CASCADE, related_name="calendario_modulo")
    periodo = models.CharField(max_length=100)
    numero_horas = models.IntegerField()
    numero_semanas = models.IntegerField()
    
    
    
class SubModuloEducativo(Base, OwnerBaseModel, SoftDeleteModel):
    modulo = models.ForeignKey(ModuloEducativo, on_delete=models.CASCADE, related_name="submodulos")
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.IntegerField(default=0)
    path_class = models.CharField(null=True, blank=True, max_length=100)
    
    
    
class MaterialModulos(BaseFileEntity, SoftDeleteModel, OwnerBaseModel):
    modulo = models.ForeignKey(ModuloEducativo, on_delete=models.CASCADE, related_name="materiales", null=True, blank=True)
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.SET_NULL, related_name="materiales", null=True, blank=True)
    submodulo = models.ForeignKey(SubModuloEducativo, on_delete=models.CASCADE, related_name="materiales", null=True, blank=True)
    
    
from django.db import models
from common.models import BaseCRM, OwnerBaseModel, SoftDeleteModel


class Pipeline(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['orden']


class Etapas(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField()
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='etapas', null=True, blank=True)
    
    class Meta:
        ordering = ['orden']


class Fuentes(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    nombre = models.CharField(max_length=100)


class Estatus(BaseCRM, OwnerBaseModel, SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name="estatus", null=True, blank=True)
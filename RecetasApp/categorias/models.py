from django.db import models
from autoslug import AutoSlugField
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
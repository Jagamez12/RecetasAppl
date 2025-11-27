from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth.models import User

from categorias.models import Categoria

# Create your models here.
class Recetas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    nombre = models.CharField(max_length=100, null=False)
    slug = AutoSlugField(populate_from='nombre', unique=True, max_length=100)
    tiempo_preparacion = models.CharField(max_length=50, null=True)
    foto = models.CharField(max_length=100, null=True)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, null=False)
    
    
    def __str__(self):
        return self.nombre
    
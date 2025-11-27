from django.db import models

# Create your models here.

class Contacto(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(unique=True, blank=False, null=False)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.correo}"
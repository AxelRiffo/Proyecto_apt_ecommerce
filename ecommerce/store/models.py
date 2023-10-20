from django.db import models

# Create your models here.
from django.db import models

class Producto(models.Model):
    titulo = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f'{self.titulo}{self.precio}'

from django.db import models
from django.db.models import Min, Max
from datetime import datetime
from django.contrib.auth.models import User

class Producto(models.Model):
    titulo = models.CharField(max_length=255)
    precio = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f'{self.titulo} - Precio: ${self.precio}'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

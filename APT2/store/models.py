from django.db import models
from django.db.models import Min, Max
from datetime import datetime
from django.contrib.auth.models import User
# # REGION
class region(models.Model):
       id_region = models.BigAutoField(primary_key=True)
       nombre_region = models.CharField(max_length=100)
       def __str__(self):
           return str(self.nombre_region)
# # #Provincia
class provincia(models.Model):
       id_provincia = models.BigAutoField(primary_key=True)
       nombre_provincia = models.CharField(max_length=100)
       id_region = models.ForeignKey(region, on_delete=models.CASCADE,null=True)
       def __str__(self):
           return str(self.nombre_provincia)
# # #COMUNA
class comuna(models.Model):
       id_comuna = models.BigAutoField(primary_key=True)
       nombre_comuna = models.CharField(max_length=100)
       id_provincia = models.ForeignKey(provincia, on_delete=models.CASCADE,null=True)
       def __str__(self):
           return str(self.nombre_comuna)

class Producto(models.Model):
    titulo = models.CharField(max_length=255)
    precio = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f'{self.titulo} - Precio: ${self.precio}'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=10)
    comuna = models.ForeignKey(comuna, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.user.username

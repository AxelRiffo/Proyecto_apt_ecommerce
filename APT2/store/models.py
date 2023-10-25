from django.db import models
from django.db.models import Min, Max
from datetime import datetime
from django.contrib.auth.models import AbstractUser, Group, Permission


#TipoUsuario
class TipoUsuario(models.Model):
        id= models.CharField(primary_key=True, max_length=3)
        nombre_tipo_usuario = models.CharField(max_length=100)
        descripcion = models.CharField(max_length=100)
        def __str__(self):
            return str(self.nombre_tipo_usuario)
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

#MODELO DE USUARIO;
class customuser(AbstractUser):
        username = models.CharField(unique=True, max_length=150)
        password = models.CharField(max_length=128)
        rut =  models.CharField(max_length=100)
        id_tipo_user = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL,null=True)
        comuna = models.ForeignKey(comuna, on_delete=models.SET_NULL,null=True)

        # Define relaciones personalizadas para grupos y permisos
        groups = models.ManyToManyField(Group, related_name='customuser_groups')
        user_permissions = models.ManyToManyField(Permission, related_name='customuser_user_permissions')
        def rutt(self):
            return str(self.rut)

        def __str__(self):
            return str(self.id) + " " + str(self.username)

class Producto(models.Model):
    titulo = models.CharField(max_length=255)
    precio = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f'{self.titulo} - Precio: ${self.precio}'

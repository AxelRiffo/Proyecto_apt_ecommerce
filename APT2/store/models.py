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
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('preparacion', 'Preparación'),
        ('horno', 'Horno'),
        ('despacho', 'Despacho'),
        ('entregado', 'Entregado'),
        ('finalizado', 'Finalizado'), 
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='OrderItem')
    delivery_method = models.CharField(max_length=20)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=20)
    total = models.IntegerField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparacion')
    tiempo_estimado = models.IntegerField(default=80)  # En minutos
    def __str__(self):
        if self.user_profile is not None and self.user_profile.user is not None:
            return f'Pedido #{self.id} - Usuario: {self.user_profile.user.username}'
        else:
            return f'Pedido #{self.id} - Usuario: Usuario no disponible'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'Pedido #{self.order.id} - Producto: {self.producto.titulo}'

class Contacto(models.Model):
    correo = models.EmailField()
    descripcion = models.TextField()
    valoracion = models.PositiveIntegerField()
    mostrar_comentarios = models.BooleanField(default=False)

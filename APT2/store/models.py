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
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='OrderItem')
    delivery_method = models.CharField(max_length=20)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Pedido #{self.id} - Usuario: {self.user_profile.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'Pedido #{self.order.id} - Producto: {self.producto.titulo}'

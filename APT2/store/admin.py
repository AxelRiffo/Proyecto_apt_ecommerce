from django.contrib import admin
from .models import Producto, UserProfile, Order, Contacto

# Register your models here.
admin.site.register(Producto),
admin.site.register(UserProfile),
admin.site.register(Order),
admin.site.register(Contacto),
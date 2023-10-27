from django.contrib import admin
from .models import Producto, comuna, TipoUsuario, region, provincia

# Register your models here.
admin.site.register(Producto),
admin.site.register(comuna),
admin.site.register(TipoUsuario)
admin.site.register(region)
admin.site.register(provincia)

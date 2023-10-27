from django.contrib import admin
from .models import Producto, comuna, region, provincia, UserProfile

# Register your models here.
admin.site.register(Producto),
admin.site.register(comuna),
admin.site.register(region)
admin.site.register(provincia)
admin.site.register(UserProfile)

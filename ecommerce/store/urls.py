from django.urls import path
from . import views
from store.views import store, agregar_producto, eliminar_producto, restar_producto, limpiar_carrito
urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('registro/', views.registro, name="registro"),
    path('login/', views.iniciar_sesion, name="login"),
    path('cuenta/', views.cuenta, name="cuenta"),
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
<<<<<<< Updated upstream
=======
    
>>>>>>> Stashed changes
]

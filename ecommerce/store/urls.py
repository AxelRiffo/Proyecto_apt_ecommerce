from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('ingreso/', views.ingreso, name="ingreso"),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name="agregar_al_carrito"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('registro/', views.registro, name="registro"),
    path('login/', views.iniciar_sesion, name="login"),
    path('cuenta/', views.cuenta, name="cuenta"),
]

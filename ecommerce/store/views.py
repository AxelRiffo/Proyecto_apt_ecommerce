from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Producto
from .forms import RegistroForm, InicioSesionForm

def store(request):
    productos = Producto.objects.all()

    for producto in productos:
        precio_formateado = "${:,.0f}".format(producto.precio).replace(",", ".")
        producto.precio_formateado = precio_formateado

    context = {'productos': productos}
    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def login(request):
    context = {}
    return render(request, 'store/login.html', context)

def registro(request):
    context = {}
    return render(request, 'store/registro.html', context)

def cuenta(request):
    context = {}
    return render(request, 'store/cuenta.html',context)
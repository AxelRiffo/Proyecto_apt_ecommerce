from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import JsonResponse
from decimal import Decimal
from .Carrito import Carrito
from django.db import IntegrityError


from .models import Producto
from .Carrito import Carrito


def store(request):
    productos = Producto.objects.all()

    for producto in productos:
        precio_formateado = "${:,.0f}".format(
            producto.precio).replace(",", ".")
        producto.precio_formateado = precio_formateado

    context = {'productos': productos}
    return render(request, 'store/store.html', context)


def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("store")


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("store")


def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("store")


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("store")


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)


def signup(request):
    if request.method == 'GET':
        return render(request, 'store/signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save
                login(request, user)
                return redirect("store")
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'User already exists'
                })
        return render(request, 'store/signup.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

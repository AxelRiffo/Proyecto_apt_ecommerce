from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Producto
from .forms import RegistroForm, InicioSesionForm
from .Carrito import Carrito



def store(request):
    productos = Producto.objects.all()

    for producto in productos:
        precio_formateado = "${:,.0f}".format(producto.precio).replace(",", ".")
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

def registro(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            # Guardar el usuario
            usuario = formulario.save()
            messages.success(request, 'Registro exitoso.')
        else:
            messages.error(request, 'Hubo un error en el registro. Por favor, verifica los datos.')

    else:
        formulario = RegistroForm()

    return render(request, 'store/registro.html', {'registro_form': formulario})

def iniciar_sesion(request):
    if request.method == 'POST':
        formulario = InicioSesionForm(request.POST)
        if formulario.is_valid():
            email = formulario.cleaned_data['email']
            password = formulario.cleaned_data['password']
            # Autenticar al usuario utilizando el correo electrónico y la contraseña
            usuario = authenticate(request, username=email, password=password)

            if usuario is not None:
                # Iniciar sesión si la autenticación es exitosa
                login(request, usuario)
                return redirect('cuenta')
            else:
                messages.error(request, 'Credenciales inválidas. Verifica tu correo electrónico y contraseña.')
        else:
            messages.error(request, 'Hubo un error en el inicio de sesión. Verifica los datos.')
    else:
        formulario = InicioSesionForm()

    return render(request, 'store/login.html', {'inicio_sesion_form': formulario})

def cuenta(request):
    context = {}
    return render(request, 'store/cuenta.html',context)
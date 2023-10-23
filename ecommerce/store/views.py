from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Producto
from .forms import RegistroForm

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

def iniciar_sesion(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            email = formulario.cleaned_data['email']  # El campo 'username' ahora almacena el correo electrónico.
            password = formulario.cleaned_data['password']
            usuario = authenticate(request, email=email, password=password)

            if usuario is not None:
                login(request, usuario)
                return redirect('cuenta')  # Cambia 'cuenta' al nombre de tu vista de cuenta si es necesario.
            else:
                messages.error(request, 'Credenciales inválidas. Verifica tu correo electrónico y contraseña.')
        else:
            messages.error(request, 'Hubo un error en el inicio de sesión. Verifica los datos.')

    formulario = AuthenticationForm()
    return render(request, 'store/login.html', {'inicio_sesion_form': formulario})

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

def cuenta(request):
    context = {}
    return render(request, 'store/cuenta.html',context)
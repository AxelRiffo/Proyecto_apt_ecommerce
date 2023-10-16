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

def ingreso(request):
    registro_form = RegistroForm()
    inicio_sesion_form = InicioSesionForm()
    if request.method == 'POST':
        registro_form = RegistroForm(request.POST)
        inicio_sesion_form = InicioSesionForm(request.POST)
        if registro_form.is_valid():
            username = registro_form.cleaned_data['username']
            email = registro_form.cleaned_data['email']
            password = registro_form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, '¡Registro exitoso!')
            return redirect('account')
        if inicio_sesion_form.is_valid():
            email = inicio_sesion_form.cleaned_data['email']
            password = inicio_sesion_form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.username}!')
            else:
                messages.error(request, 'Inicio de sesión no válido. Por favor, verifique sus credenciales.')

    return render(request, 'store/ingreso.html', {'registro_form': registro_form, 'inicio_sesion_form': inicio_sesion_form})

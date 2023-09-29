from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Producto
from .forms import RegistroForm, InicioSesionForm

def store(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, password=password)
            return redirect('/')  # Página principal o donde desees redirigir después del registro
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = InicioSesionForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Página principal o donde desees redirigir después del inicio de sesión
    else:
        form = InicioSesionForm()

    return render(request, 'inicio_sesion.html', {'form': form})

def store(request):
    productos = Producto.objects.all()

    # Formatear el precio con punto como separador de miles y coma como separador decimal
    for producto in productos:
        precio_formateado = "${:,.0f}".format(producto.precio).replace(",", ".")
        producto.precio_formateado = precio_formateado

    context = {'productos': productos}
    return render(request, 'store/store.html', context)
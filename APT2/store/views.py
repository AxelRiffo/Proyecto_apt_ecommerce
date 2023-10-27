from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db import IntegrityError
from .models import Producto
from .Carrito import Carrito
from django.contrib.auth import authenticate

# DETALLES FUNCIONALES EN EL SISTEMA
from django.contrib import messages



def store(request):
    productos = Producto.objects.all()

    for producto in productos:
        precio_formateado = "${:,.0f}".format(
            producto.precio).replace(",", ".")
        producto.precio_formateado = precio_formateado

    context = {'productos': productos}
    return render(request, 'store.html', context)


def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("Store")


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("Store")


def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Store")


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("Store")

from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm()
        })
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('Cuenta')
        else:
            return render(request, 'signup.html', {
                'form': form,
                "error": 'Hubo un error en el registro'
            })

def cuenta(request):
    return render(request, 'cuenta.html')


def signout(request):
    logout(request)
    return redirect('Store')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })



#Sirve pa cargar datos en las tablas por eso ta comentao iwal q su url pa la carga
#from django.http import HttpResponse
#import csv
#def load_data(request):
#    with open(r'C:\Users\damia\OneDrive\Documentos\GitHub\Proyecto_apt_ecommerce\APT2\comuna.csv', 'r') as f:
#        reader = csv.reader(f)
#        next(reader)  # Saltar el encabezado
#        for row in reader:
#            if len(row) >= 3:  # Asegurarse de que hay al menos 3 columnas
                # Asume que el nombre de la comuna está en la primera columna
                # el id de la comuna está en la segunda columna
                # y el id de la provincia está en la tercera columna
#                nombre = row[0]
#                id = row[1]
#                provincia_id = row[2]
#                if provincia_id:  # Verificar que provincia_id no esté vacío
#                    provincia_obj = provincia.objects.get(id_provincia=provincia_id)
#                    comuna.objects.create(id_comuna=id, nombre_comuna=nombre, id_provincia=provincia_obj)  
#    return HttpResponse("Datos cargados con éxito")

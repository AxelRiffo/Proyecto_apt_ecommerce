from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db import IntegrityError
from .models import Producto, provincia, region, comuna
from .Carrito import Carrito

# DETALLES FUNCIONALES EN EL SISTEMA
from django.contrib import messages

# MODELOS Y FORMULARIOS
from .forms import CustomUserCreationForm


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


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('Cuenta')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })


def cuenta(request):
    return render(request, 'cuenta.html')


def signout(request):
    logout(request)
    return redirect('Store')


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Inicio de sesión exitoso
            user = form.get_user()
            login(request, user)
            return redirect('Cuenta')
        else:
            # Inicio de sesión fallido
            error_message = "Credenciales incorrectas. Inténtalo de nuevo."
    else:
        form = AuthenticationForm()

    return render(request, 'signin.html', {
        'form': form,
        'error_message': error_message if 'error_message' in locals() else None
    })

# REGISTRO SITE;


def registro(request):
    dato = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "te has registrado correctamente")
        return redirect('login')
    return render(request, 'registration/registro.html', dato)




# ta comentado pq sirve pa cargar grandes cantidades de datos al ingresar a esa url

#from django.http import HttpResponse
#import csv
#def load_data(request):
#        reader = csv.reader(f)
#        next(reader)  # Saltar el encabezado
#       for row in reader:
#            if len(row) >= 3:  # Asegurarse de que hay al menos 3 columnas
#                # Asume que el nombre de la comuna está en la primera columna
#                # el id de la comuna está en la segunda columna
#                # y el id de la provincia está en la tercera columna
#                nombre = row[0]
#                id = row[1]
#                provincia_id = row[2]
#                if provincia_id:  # Verificar que provincia_id no esté vacío
#                    provincia_obj = provincia.objects.get(id_provincia=provincia_id)
#                    comuna.objects.create(id_comuna=id, nombre_comuna=nombre, id_provincia=provincia_obj)  
#    return HttpResponse("Datos cargados con éxito")
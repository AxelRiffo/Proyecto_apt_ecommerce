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
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Cuenta')
            else:
                messages.error(request, "Las credenciales de inicio de sesión no son válidas.")
        else:
            messages.error(request, "Hubo un error en el formulario.")
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})


def checkout(request):
    return render(request, 'checkout.html')


from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def cuenta(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)

        if form.is_valid():
            print(form.errors)
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')

            user = User.objects.get(username=request.user.username)

            if username:
                user.username = username
            if email:
                user.email = email
            if old_password and new_password:
                if not request.user.check_password(old_password):
                    form.add_error('old_password', 'La antigua contraseña no es correcta.')
                else:
                    user.set_password(new_password)

            user.save()

            # Actualiza la contraseña del usuario en la sesión actual
            update_session_auth_hash(request, user)

            return redirect('Cuenta')
        else:
            return render(request, 'cuenta.html', {
                'form': form,
                "error": form.errors
            })
    else:
        form = EditProfileForm(initial={
            'username': request.user.username,
            'email': request.user.email,
        })
        return render(request, 'cuenta.html', {'form': form})

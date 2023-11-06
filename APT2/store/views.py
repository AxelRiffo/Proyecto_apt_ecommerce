from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .models import Producto, Order, OrderItem
from .Carrito import Carrito
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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

@login_required
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

def calculate_total(order):
    total = 0
    order_items = OrderItem.objects.filter(order=order)

    for item in order_items:
        total += item.producto.precio * item.cantidad

    # Agregar el costo de entrega, si corresponde
    if order.delivery_method == 'delivery':
        total += order.total

    return total

@login_required
def checkout(request):
    if request.method == 'POST':
        # Obtener los datos del formulario de checkout
        delivery_method = request.POST['delivery_method']
        comuna = request.POST['comuna']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        payment_method = request.POST['payment_method']
        
        # Crear una nueva instancia de Order
        order = Order(
            user_profile=request.user.userprofile,  # Asegúrate de que el usuario esté autenticado
            delivery_method=delivery_method,
            comuna=comuna,
            direccion=direccion,
            telefono=telefono,
            payment_method=payment_method,
            total=0,  # Debes calcular el total correctamente
        )
        order.save()

        # Obtener los productos del carrito
        carrito = Carrito(request)
        for item in carrito:
            producto = item['producto']
            cantidad = item['cantidad']
            # Crear una instancia de OrderItem
            order_item = OrderItem(order=order, producto=producto, cantidad=cantidad)
            order_item.save()
        
        # Calcula el total real y actualiza la orden
        order.total = calculate_total(order)
        order.save()

        # Limpia el carrito
        carrito.clear()

        # Redirige a una página de confirmación u otra página
        return HttpResponse('¡Orden creada exitosamente!')

    return render(request, 'checkout.html')








# Ni perra idea de que es esto pero no lo voy a tocar :)

from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

@login_required
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

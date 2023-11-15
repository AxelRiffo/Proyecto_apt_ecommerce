from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Order, OrderItem
from .Carrito import Carrito
from django.urls import reverse
from django.utils import timezone

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

    if order.delivery_method == 'delivery':
        total += order.total

    return total

@login_required
def checkout(request):
    if request.method == 'POST':
        delivery_method = request.POST['delivery_method']
        comuna = request.POST['comuna']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        payment_method = request.POST['payment_method']
        order = Order(
            user_profile=request.user.userprofile,
            delivery_method=delivery_method,
            comuna=comuna,
            direccion=direccion,
            telefono=telefono,
            payment_method=payment_method,
            total=0,
        )
        order.save()
        carrito = Carrito(request)
        for item in carrito:
            producto = item['producto']
            cantidad = item['cantidad']
            order_item = OrderItem(order=order, producto=producto, cantidad=cantidad)
            order_item.save()        
        order.total = calculate_total(order)
        order.save()
        carrito.clear()
        return HttpResponse('¡Orden creada exitosamente!')

    return render(request, 'checkout.html')


from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

@login_required
def cuenta(request):
    # Busca todos los pedidos del usuario actual
    todos_pedidos = Order.objects.filter(user_profile__user=request.user)
    # Busca solo los pedidos del usuario actual que no estén 'entregado' o 'finalizado'
    pedidos_seguimiento = todos_pedidos.exclude(status__in=['entregado', 'finalizado'])
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

            update_session_auth_hash(request, user)

            return redirect('Cuenta')
        else:
            return render(request, 'cuenta.html', {
                'form': form,
                "error": form.errors,
                'todos_pedidos': todos_pedidos,
                'pedidos_seguimiento': pedidos_seguimiento
            })
    else:
        form = EditProfileForm(initial={
            'username': request.user.username,
            'email': request.user.email,
        })
        return render(request, 'cuenta.html',  {'form': form, 'todos_pedidos': todos_pedidos, 'pedidos_seguimiento': pedidos_seguimiento})

def order_dashboard(request):
    pedidos = Order.objects.all()
    return render(request, 'panel.html', {'pedidos': pedidos})

from django.utils import timezone

def pedido_update(request, pk):
    pedido = get_object_or_404(Order, pk=pk)
    # Cambia el estado del pedido al siguiente estado
    if pedido.status == 'preparacion':
        pedido.status = 'horno'
        pedido.tiempo_estimado = 50  # Tiempo estimado para 'horno'
    elif pedido.status == 'horno':
        pedido.status = 'despacho'
        pedido.tiempo_estimado = 20  # Tiempo estimado para 'despacho'
    elif pedido.status == 'despacho':
        pedido.status = 'entregado'
        pedido.tiempo_estimado = 0   # No hay tiempo estimado para 'entregado'
    pedido.save()
    return redirect('order_dashboard')




def pedido_finalizado(request, pk):
    pedido = get_object_or_404(Order, pk=pk)
    # Cambia el estado del pedido a 'finalizado'
    pedido.status = 'finalizado'
    pedido.save()
    return redirect('order_dashboard')


def aboutus(request):
    return render(request, 'aboutus.html')

from .forms import ContactoForm
from .models import Contacto

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Contacto')
    else:
        form = ContactoForm()

    comentarios = Contacto.objects.filter(mostrar_comentarios=True)

    return render(request, 'contacto.html', {'form': form, 'comentarios': comentarios})
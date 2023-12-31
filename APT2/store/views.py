from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Order, OrderItem,  UserProfile
from .Carrito import Carrito
from django.urls import reverse
from django.utils import timezone
from .forms import CheckoutForm
from django.http import JsonResponse
import mercadopago
from django.conf import settings
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
    print(request.POST)  # Imprime los datos del formulario
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            delivery_method = form.cleaned_data['delivery_method']
            comuna = form.cleaned_data['comuna']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            payment_method = form.cleaned_data['payment_method']


            
            # Crear una nueva instancia de Order y asignar los valores
            order = Order(
                user_profile=request.user.userprofile if hasattr(request.user, 'userprofile') else None,
                delivery_method=delivery_method,
                comuna=comuna,
                direccion=direccion,
                telefono=telefono,
                payment_method=payment_method,
                total=calculate_total
            )

            # Guardar el acumulado del carrito como total de la orden
            carrito = Carrito(request)
            total_carrito = sum(int(item.get('acumulado', 0)) for item in carrito)
            order.total = total_carrito if total_carrito > 0 else None

            # Guardar la orden en la base de datos antes de agregar los detalles de los productos
            order.save()

            # Ahora, debes agregar los detalles de los productos a través de OrderItem.
            # Recorre los productos en el carrito y crea instancias de OrderItem para cada uno.
            for item in carrito:
                order_item = OrderItem(
                    order=order,
                    producto=item['producto'],
                    cantidad=item['cantidad'],
                )
                order_item.save()

            # Limpia el carrito después de guardar en la base de datos
            limpiar_carrito(request)


    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})

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




import mercadopago
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem, Producto, UserProfile
from django.http import JsonResponse

def procesar_pago(request):
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    # Obtén los productos del carrito
    carrito = Carrito(request)
    
    # Crea una lista para almacenar los items del carrito
    items = []
    
    # Recorre los productos en el carrito y agrega cada uno a la lista de items
    for item in carrito:
        items.append({
            "title": item['producto'].titulo, 
            "quantity": item['cantidad'],
            "currency_id": "CLP", 
            "unit_price": item['producto'].precio  
        })
    
    preference = {
        "items": items
    }

    # Crea una instancia de UserProfile o recupera la existente
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Crea una instancia de Order y guárdala en la base de datos
    order = Order.objects.create(
        user_profile=user_profile,
        delivery_method=('delivery'),  # Obtiene el método de entrega del POST request
        comuna=('CerroNavia'),  # Obtiene la comuna del POST request
        direccion=('Janequeo 6485'),  # Obtiene la dirección del POST request
        telefono=('988460249'),  # Obtiene el teléfono del POST request
        payment_method=('MercadoPago'),  # Obtiene el método de pago del POST request
        total=('10000'),  # Obtiene el total del POST request
        status='preparacion'  # Agrega tu lógica aquí
    )

    # Agrega los productos a la orden
    for item in carrito:
        OrderItem.objects.create(
            order=order,
            producto=item['producto'],
            cantidad=item['cantidad']
        )

    # Guarda la orden en la base de datos
    order.save()
    carrito.limpiar()

    # Crea la preferencia de pago
    preference_result = sdk.preference().create(preference)
    
    # Obtener la URL de pago desde la respuesta
    payment_url = preference_result['response']['sandbox_init_point']

    # Redirigir al usuario a la URL de pago
    return redirect(payment_url)


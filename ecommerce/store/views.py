from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Producto, Cart, CartItem
from .forms import RegistroForm, InicioSesionForm
from django.shortcuts import render, redirect


def store(request):
    productos = Producto.objects.all()

    # Formatear el precio con punto como separador de miles y coma como separador decimal
    for producto in productos:
        precio_formateado = "${:,.0f}".format(producto.precio).replace(",", ".")
        producto.precio_formateado = precio_formateado

    context = {'productos': productos}
    return render(request, 'store/store.html', context)

def cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.cartitem_set.all()

    total_price = sum(item.product.precio * item.quantity for item in cart_items)
    total_price_formatted = "${:,.2f}".format(total_price).replace(",", ".")

    context = {
        'cart_items': cart_items,
        'total_price': total_price_formatted,
    }

    return render(request, 'store/cart.html', context)

def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Producto, pk=product_id)

    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def remove_from_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Producto, pk=product_id)

    cart, created = Cart.objects.get_or_create(user=user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')



def carrito(request):
    carrito = request.session.get('carrito', [])
    
    # Obtén los productos en el carrito
    productos_en_carrito = Producto.objects.filter(id__in=carrito)
    
    # Calcula el precio total del carrito
    precio_total = sum(producto.precio for producto in productos_en_carrito)
    
    context = {'productos_en_carrito': productos_en_carrito, 'precio_total': precio_total}
    return render(request, 'store/cart.html', context)


# Resto de tus vistas existentes


def agregar_al_carrito(request, producto_id):
    producto = Producto.objects.get(pk=producto_id)
    
    # Obtén el carrito actual del usuario desde la sesión o crea uno si no existe
    carrito = request.session.get('carrito', [])
    
    # Agrega el ID del producto al carrito
    carrito.append(producto.id)
    
    # Guarda el carrito en la sesión
    request.session['carrito'] = carrito
    
    return redirect('carrito')








def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def ingreso(request):
    registro_form = RegistroForm()  # Define las variables fuera del bloque condicional
    inicio_sesion_form = InicioSesionForm()

    if request.method == 'POST':
        registro_form = RegistroForm(request.POST)
        inicio_sesion_form = InicioSesionForm(request.POST)
        if registro_form.is_valid():
            # Procesar registro
            username = registro_form.cleaned_data['username']
            email = registro_form.cleaned_data['email']
            password = registro_form.cleaned_data['password']
            # Crear usuario
            user = User.objects.create_user(username=username, email=email, password=password)
            # Iniciar sesión
            login(request, user)
            return redirect('/')  # Página principal después del registro
        elif inicio_sesion_form.is_valid():
            # Procesar inicio de sesión
            username = inicio_sesion_form.cleaned_data['username']
            password = inicio_sesion_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Página principal después del inicio de sesión

    return render(request, 'store/ingreso.html', {'registro_form': registro_form, 'inicio_sesion_form': inicio_sesion_form})

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = UserProfile(user=user)
            profile.save()
        return user
    
    
from django import forms

class EditProfileForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario:', required=False)
    email = forms.EmailField(label='Correo electrónico:', required=False)
    old_password = forms.CharField( 
        label='Contraseña Antigua:',
        widget=forms.PasswordInput, 
        required=False,
        error_messages={
            'invalid': 'La antigua contraseña no es correcta.'
        }
    )
    new_password = forms.CharField(label='Contraseña nueva:', widget=forms.PasswordInput, required=False)

from .models import Contacto

class ContactoForm(forms.ModelForm):
    valoracion = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id': 'valoracion-id'}),
        required=False,
        initial=0,  # Establecer el valor predeterminado en 0
    )

    class Meta:
        model = Contacto
        fields = ['valoracion', 'correo', 'descripcion']
        widgets = {
            'mostrar_comentarios': forms.HiddenInput(),
        }

# En tu archivo forms.py
from django import forms

class CheckoutForm(forms.Form):
    DELIVERY_CHOICES = [
        ('delivery', 'Delivery'),
        ('local_pickup', 'Retiro en local'),
    ]
    PAYMENT_CHOICES = [
        ('mercadopago', 'MercadoPago'),
        ('efectivo', 'En efectivo'),
    ]

    delivery_method = forms.ChoiceField(choices=DELIVERY_CHOICES, widget=forms.RadioSelect)
    comuna = forms.ChoiceField(choices=[('Pudahuel', 'Pudahuel'), ('CerroNavia', 'Cerro Navia')], required=False)
    direccion = forms.CharField(max_length=255, required=False)
    telefono = forms.CharField(max_length=20, required=False)
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)

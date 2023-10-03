from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        # Validaciones adicionales para la contraseña
        if len(password) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('La contraseña debe contener al menos una mayúscula.')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('La contraseña debe contener al menos un número.')

        return cleaned_data

class InicioSesionForm(AuthenticationForm):
    username = forms.EmailField(label='Correo Electrónico')
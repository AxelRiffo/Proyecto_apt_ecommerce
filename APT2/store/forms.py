from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import customuser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = customuser
        fields = (
            'rut',
            'email',
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
            'id_tipo_user',
            'comuna',
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Personaliza los mensajes de error para los campos de contraseña
        self.fields['password1'].error_messages = {
            'password_mismatch': 'Las contraseñas no coinciden.',
            'password_too_short': 'La contraseña debe tener al menos 8 caracteres.',
            'password_common': 'La contraseña es muy común.',
            'password_entirely_numeric': 'La contraseña no puede ser completamente numérica.',
            # Agrega otros mensajes personalizados si es necesario
        }

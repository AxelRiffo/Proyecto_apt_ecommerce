from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import customuser
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = customuser
        fields =  (
            'email',
            'username', 
            'first_name', 
            'last_name', 
            'id_tipo_user', 
            'comuna',
            'password1', 
            'password2',
            'rut'
            )
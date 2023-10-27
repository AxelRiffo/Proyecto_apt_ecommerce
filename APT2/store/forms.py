from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import comuna

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    rut = forms.CharField(max_length=10)
    comuna = forms.ModelChoiceField(queryset=comuna.objects.all())

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "rut", "comuna", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.comuna = self.cleaned_data['comuna']  # Guarda la comuna en el usuario
        user.rut = self.cleaned_data['rut'] 
        if commit:
            user.save()
        return user

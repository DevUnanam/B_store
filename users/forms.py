from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "occupant"  # Default role
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-input"}))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "apartment_number", "profile_image"]

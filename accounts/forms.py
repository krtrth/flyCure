from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import PatientProfile


class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=False)
    country = forms.CharField(max_length=100, required=False)
    phone_whatsapp = forms.CharField(max_length=32, required=False, label="WhatsApp number")
    preferred_language = forms.CharField(max_length=50, required=False, initial="English")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "country",
            "phone_whatsapp",
            "preferred_language",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
            PatientProfile.objects.create(
                user=user,
                country=self.cleaned_data.get("country", ""),
                phone_whatsapp=self.cleaned_data.get("phone_whatsapp", ""),
                preferred_language=self.cleaned_data.get("preferred_language") or "English",
            )
        return user


class PatientLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .mixins import is_doctor, is_hospital, is_patient
from .models import PatientProfile


class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=False)
    country = forms.CharField(max_length=100, required=False)
    phone_whatsapp = forms.CharField(max_length=32, required=False, label="WhatsApp number")
    mobile = forms.CharField(max_length=32, required=False)
    preferred_language = forms.CharField(max_length=50, required=False, initial="English")
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=[("", "Select")] + list(PatientProfile.Gender.choices), required=False)
    height_cm = forms.DecimalField(required=False, min_value=50, max_value=250, decimal_places=1, label="Height (cm)")
    weight_kg = forms.DecimalField(required=False, min_value=20, max_value=400, decimal_places=1, label="Weight (kg)")

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
            "mobile",
            "preferred_language",
            "date_of_birth",
            "gender",
            "height_cm",
            "weight_kg",
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
                mobile=self.cleaned_data.get("mobile", ""),
                preferred_language=self.cleaned_data.get("preferred_language") or "English",
                date_of_birth=self.cleaned_data.get("date_of_birth"),
                gender=self.cleaned_data.get("gender", ""),
                height_cm=self.cleaned_data.get("height_cm"),
                weight_kg=self.cleaned_data.get("weight_kg"),
            )
        return user


class PatientProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()

    class Meta:
        model = PatientProfile
        fields = (
            "country",
            "phone_whatsapp",
            "mobile",
            "preferred_language",
            "date_of_birth",
            "gender",
            "height_cm",
            "weight_kg",
        )
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance.user
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email
        self.fields["height_cm"].label = "Height (cm)"
        self.fields["weight_kg"].label = "Weight (kg)"

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data.get("last_name", "")
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile.save()
        return profile


class PatientLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if is_doctor(user) or is_hospital(user):
            raise forms.ValidationError(
                "This is a provider account. Use the hospital and doctor login instead.",
                code="provider-account",
            )
        if not is_patient(user):
            raise forms.ValidationError(
                "This login is for patients. Create a patient account or use provider login.",
                code="not-patient",
            )


class ProviderLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        doctor = is_doctor(user)
        hospital = is_hospital(user)
        if doctor and hospital:
            raise forms.ValidationError(
                "This account is linked to both a doctor and a hospital. Ask an administrator to fix it.",
                code="dual-role",
            )
        if not doctor and not hospital:
            if is_patient(user):
                raise forms.ValidationError(
                    "This is a patient account. Use patient login instead.",
                    code="patient-account",
                )
            raise forms.ValidationError(
                "This account is not linked to a doctor or hospital profile.",
                code="not-provider",
            )

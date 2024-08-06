import re
from django import forms

from .models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(
        max_length=40,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email"}
        ),
    )
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    profile_id = forms.CharField(
        max_length=30,
        label="profile_id",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your profile_id",
                "pattern": "[A-Za-z0-9_.]{3,}",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already exists")
        return email

    def clean_profile_id(self):
        profile_id = self.cleaned_data["profile_id"]
        patt = r"[A-Za-z0-9_.]{3,}"
        if not re.match(patt, profile_id):
            raise forms.ValidationError("Profile Id is not matched")
        if User.objects.filter(profile_id=profile_id).exists():
            raise forms.ValidationError("Profile Id is already exists")
        return profile_id


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=40,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email"}
        ),
    )
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())

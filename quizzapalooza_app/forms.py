from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your password'}))


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your password'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your password again'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class JoinQuizForm(forms.Form):
    session_id = forms.IntegerField()
    nickname = forms.CharField()

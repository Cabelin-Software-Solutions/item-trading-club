from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Proposal

class AlertForm(forms.Form):
    error = forms.CharField(max_length=255, required=False)
    message = forms.CharField(max_length=255, required=False)

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

class ItemForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.CharField(max_length=255)

class DeleteItemForm(forms.Form):
    id = forms.IntegerField()

class EditItemForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.CharField(max_length=255)

class EditUserForm(forms.Form):
    username = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=255, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=255, label='Repeat Password')

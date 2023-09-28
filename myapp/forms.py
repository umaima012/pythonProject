from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'myapp/form.html'
    authentication_form = AuthenticationForm

class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
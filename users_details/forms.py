

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import TextField
from django.forms import EmailField, ModelForm, CharField, Form
from .models import ProfileDetails


class RegisterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(Form):
    email = CharField(label="username")
    password = CharField(label="Password")

class EditProfile(ModelForm):
    class Meta:
        model = ProfileDetails
        fields = ["full_name", "birthday", "image"]

class EditAdminDetails(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
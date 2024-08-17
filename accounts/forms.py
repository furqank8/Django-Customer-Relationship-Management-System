from django.forms import ModelForm
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# Form for creating or updating an Order
class OrderForm(ModelForm):
    """
    A form for creating or updating an Order instance.
    Inherits from Django's ModelForm to automatically generate form fields based on the Order model.
    """
    class Meta:
        model = Order  # Specify the model associated with this form
        fields = '__all__'  # Include all fields from the Order model in the form

# Form for creating a new user
class CreateUserForm(UserCreationForm):
    """
    A form for creating a new User instance with username, email, and password fields.
    Inherits from Django's UserCreationForm to include built-in user creation functionality.
    """
    class Meta:
        model = User  # Specify the model associated with this form (Django's built-in User model)
        fields = ['username', 'email', 'password1', 'password2']  # Include username, email, and password fields

from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.")
    
    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
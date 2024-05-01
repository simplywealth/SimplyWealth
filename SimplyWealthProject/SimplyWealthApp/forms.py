from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.")
    
    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']



class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

    
class FriendSearchForm(forms.ModelForm):
    query = forms.CharField(max_length=100, label='Search for Friends')

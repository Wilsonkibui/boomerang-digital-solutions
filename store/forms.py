from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomerCheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}))
    location = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Delivery Address / Location', 'rows': 3}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Optional Notes', 'rows': 2}))

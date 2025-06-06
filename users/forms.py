from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from core.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username","email","role","phone_number","address","password1","password2"]

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["username","password"]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','phone_number','address']
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.Textarea(attrs={'class':'form-control','rows' : 2}),
        }
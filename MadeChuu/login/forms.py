from django import forms
from main.models import *

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'email', 'phone_num', 'password','gender','birth_date','birth_month','birth_year','province','district']
        widgets = {
            'password': forms.PasswordInput(),
        }
from django.forms import ModelForm
from django import forms
from .models import *

class ChatMessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Type a message...'}),
        }
        

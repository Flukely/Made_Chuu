# tracking/forms.py
from django import forms
from main.models import Refund

class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['refund_type', 'bank_name', 'refund_number', 'account_name']
        widgets = {
            'refund_type': forms.Select(attrs={'class': 'form-select', 'id': 'refund_type'}),
            'bank_name': forms.Select(attrs={'class': 'form-select', 'id': 'bank_name'}),
            'refund_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'refund_number', 'placeholder': 'Number'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'account_name', 'placeholder': 'Name'}),
        }
        labels = {
            'refund_type': 'ประเภทการคืนเงิน',
            'bank_name': 'ธนาคาร',
            'refund_number': 'หมายเลข',
            'account_name': 'ชื่อบัญชี',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['refund_type'].choices = Refund.REFUND_TYPE_CHOICES
        self.fields['bank_name'].choices = Refund.BANK_NAME_CHOICES

        # Initialize fields to be not required
        self.fields['bank_name'].required = False
        self.fields['refund_number'].required = False
        self.fields['account_name'].required = False
        
        # set label to blank initially
        self.fields['bank_name'].label = 'ธนาคาร' 
        self.fields['refund_number'].label = 'หมายเลข'
        self.fields['account_name'].label = 'ชื่อบัญชี'

        if self.data:
            refund_type = self.data.get('refund_type')
            if refund_type == 'bank':
                self.fields['bank_name'].required = True
                self.fields['refund_number'].required = True
                self.fields['account_name'].required = True
            elif refund_type == 'promptpay':
                self.fields['refund_number'].required = True
                self.fields['account_name'].required = True

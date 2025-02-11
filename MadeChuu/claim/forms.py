from django import forms
from main.models import Claim

class ClaimForm(forms.ModelForm):
    REASON_CHOICES = [
        ('ฉันไม่ได้รับพัสดุของคำสั่งซื้อนี้', 'ฉันไม่ได้รับพัสดุของคำสั่งซื้อนี้'),
        ('สินค้าเสียหาย', 'สินค้าเสียหาย'),
        ('สินค้าไม่ตรงตามที่สั่ง', 'สินค้าไม่ตรงตามที่สั่ง'),
        ('อื่น ๆ', 'อื่น ๆ'),
    ]

    reason = forms.ChoiceField(choices=REASON_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    contact_method = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรอกช่องทางการติดต่อของคุณ'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'กรอกปัญหาที่คุณพบ'}))
    claim_image = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    claim_video = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    promtpay_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรอกหมายเลขพร้อมเพย์ของคุณ'}))

    class Meta:
        model = Claim
        fields = ['reason', 'contact_method', 'comment', 'claim_image', 'claim_video', 'promtpay_number']
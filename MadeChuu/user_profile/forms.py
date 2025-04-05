from django import forms
from django.contrib.auth.forms import UserChangeForm
from main.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'user_name',
            'email',
            'phone_num',
            'birth_date',
            'gender',
            'address',
            'district',
            'province',
            'postal_code'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'phone_num': forms.TextInput(attrs={'pattern': '[0-9]{10}'}),
        }
        labels = {
            'user_name': 'ชื่อผู้ใช้',
            'phone_num': 'เบอร์โทรศัพท์',
            'birth_date': 'วันเกิด',
            'postal_code': 'รหัสไปรษณีย์'
        }
    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')
        if phone_num and (not phone_num.isdigit() or len(phone_num) != 10):
            raise forms.ValidationError("กรุณากรอกเบอร์โทรศัพท์ 10 หลักเป็นตัวเลขเท่านั้น")
        return phone_num

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if postal_code and (not postal_code.isdigit() or len(postal_code) != 5):
            raise forms.ValidationError("รหัสไปรษณีย์ต้องเป็นตัวเลข 5 หลัก")
        return postal_code
    
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

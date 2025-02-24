from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    PROVINCE_CHOICES = [
        ('BKK', 'กรุงเทพมหานคร'),
        ('KBI', 'กระบี่'),
        ('KRI', 'กาญจนบุรี'),
        ('KSN', 'กาฬสินธุ์'),
        ('KPT', 'กำแพงเพชร'),
        ('KKN', 'ขอนแก่น'),
        ('CTI', 'จันทบุรี'),
        ('CCO', 'ฉะเชิงเทรา'),
        ('CBI', 'ชลบุรี'),
        ('CNT', 'ชัยนาท'),
        ('CPM', 'ชัยภูมิ'),
        ('CPN', 'ชุมพร'),
        ('CRI', 'เชียงราย'),
        ('CMI', 'เชียงใหม่'),
        ('TRG', 'ตรัง'),
        ('TRT', 'ตราด'),
        ('TAK', 'ตาก'),
        ('NYK', 'นครนายก'),
        ('NPT', 'นครปฐม'),
        ('NPM', 'นครพนม'),
        ('NMA', 'นครราชสีมา'),
        ('NST', 'นครศรีธรรมราช'),
        ('NSN', 'นครสวรรค์'),
        ('NBI', 'นนทบุรี'),
        ('NWT', 'นราธิวาส'),
        ('NAN', 'น่าน'),
        ('BKN', 'บึงกาฬ'),
        ('BRM', 'บุรีรัมย์'),
        ('PTT', 'ปทุมธานี'),
        ('PBI', 'ประจวบคีรีขันธ์'),
        ('PRI', 'ปราจีนบุรี'),
        ('PTN', 'ปัตตานี'),
        ('AYA', 'พระนครศรีอยุธยา'),
        ('PYO', 'พะเยา'),
        ('PNA', 'พังงา'),
        ('PLG', 'พัทลุง'),
        ('PCT', 'พิจิตร'),
        ('PLK', 'พิษณุโลก'),
        ('PBI', 'เพชรบุรี'),
        ('PBN', 'เพชรบูรณ์'),
        ('PRE', 'แพร่'),
        ('PKT', 'ภูเก็ต'),
        ('MSK', 'มหาสารคาม'),
        ('MDH', 'มุกดาหาร'),
        ('MHS', 'แม่ฮ่องสอน'),
        ('YST', 'ยโสธร'),
        ('YLA', 'ยะลา'),
        ('RET', 'ร้อยเอ็ด'),
        ('RNG', 'ระนอง'),
        ('RYG', 'ระยอง'),
        ('RBR', 'ราชบุรี'),
        ('LRI', 'ลพบุรี'),
        ('LPG', 'ลำปาง'),
        ('LPN', 'ลำพูน'),
        ('LEI', 'เลย'),
        ('SSK', 'ศรีสะเกษ'),
        ('SNK', 'สกลนคร'),
        ('SKA', 'สงขลา'),
        ('STN', 'สตูล'),
        ('SPK', 'สมุทรปราการ'),
        ('SKM', 'สมุทรสงคราม'),
        ('SKN', 'สมุทรสาคร'),
        ('SKW', 'สระแก้ว'),
        ('SRI', 'สระบุรี'),
        ('SBR', 'สิงห์บุรี'),
        ('STI', 'สุโขทัย'),
        ('SPB', 'สุพรรณบุรี'),
        ('SNI', 'สุราษฎร์ธานี'),
        ('SRN', 'สุรินทร์'),
        ('NKI', 'หนองคาย'),
        ('NBP', 'หนองบัวลำภู'),
        ('ATG', 'อ่างทอง'),
        ('ACR', 'อำนาจเจริญ'),
        ('UDN', 'อุดรธานี'),
        ('UTT', 'อุตรดิตถ์'),
        ('UTI', 'อุทัยธานี'),
        ('UBN', 'อุบลราชธานี'),
    ]
    
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    province = forms.ChoiceField(choices=PROVINCE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'user_name', 'address', 'district', 'province', 'postal_code', 'gender', 'birth_date', 'phone_num']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
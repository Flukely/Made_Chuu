from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect
from django import forms
from .forms import UserRegisterForm
from main.models import AdminRole, UserRole, Admin, User

# ฟอร์มเข้าสู่ระบบ
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # เพิ่มบทบาทให้กับผู้ใช้
            default_role = UserRole.objects.get(user_role_name='Customer')  # ดึงบทบาทที่มีอยู่แล้ว
            user.user_role = default_role  # ใช้ user ซึ่งเป็นอินสแตนซ์ของโมเดล User
            user.save()  # บันทึกข้อมูลลงฐานข้อมูล
            
            return redirect("index")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


# เข้าสู่ระบบ
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('AddCart')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("login")
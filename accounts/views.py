from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms
from .forms import UserRegisterForm

# ฟอร์มเข้าสู่ระบบ
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# สมัครสมาชิก
def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})

# เข้าสู่ระบบ
def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")  # ถ้าผู้ใช้ล็อกอินอยู่แล้ว ให้เปลี่ยนเส้นทางไปยังหน้าแดชบอร์ด
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # บันทึกข้อมูลผู้ใช้ใน Session
                request.session['user_id'] = user.user_id
                request.session['user_email'] = user.email
                request.session['user_name'] = user.user_name
                return redirect("index")
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

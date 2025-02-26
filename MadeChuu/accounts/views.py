from django.contrib.auth import authenticate, login, logout
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
        return redirect("product")  # ถ้าผู้ใช้ล็อกอินอยู่แล้ว ให้เปลี่ยนเส้นทางไปยังหน้าสินค้า
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # เพิ่มบทบาทให้กับผู้ใช้
            default_role = UserRole.objects.get(user_role_name='Customer')  # ดึงบทบาทที่มีอยู่แล้ว
            user.user_role = default_role  # ใช้ user ซึ่งเป็นอินสแตนซ์ของโมเดล User
            user.save()  # บันทึกข้อมูลลงฐานข้อมูล
            
            return redirect("product")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})

# เข้าสู่ระบบ
def user_login(request):
    if request.user.is_authenticated:
        return redirect("product")  # ถ้าผู้ใช้ล็อกอินอยู่แล้ว ให้เปลี่ยนเส้นทางไปยังหน้าแดชบอร์ด
    
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
                
                # บันทึกบทบาทของผู้ใช้ใน Session
                roles = AdminRole.objects.filter(admin__user=user).values_list('admin_role_name', flat=True)
                request.session['user_roles'] = list(roles)
                
                return redirect("product")
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("product")
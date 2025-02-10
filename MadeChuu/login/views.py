from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.auth.hashers import check_password
from .forms import RegisterForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_name, password FROM User WHERE user_name = %s", [username])
            user = cursor.fetchone()
        
        if user and check_password(password, user[1]):
            request.session['username'] = user[0]
            return redirect('register')  # เปลี่ยนเส้นทางไปยังหน้าโปรไฟล์หรือหน้าอื่นที่ต้องการ
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return redirect('login')
    else:
        register_form = RegisterForm()
    
    return render(request, "register.html", {'register_form': register_form})
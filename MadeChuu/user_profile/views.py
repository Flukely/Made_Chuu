from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm, PasswordChangeForm
from main.models import User

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # ดึงข้อมูลจากฟอร์ม
            user = form.save(commit=False)
            
            # อัปเดตฟิลด์ต่างๆ ตามโมเดล User
            user.user_name = form.cleaned_data['user_name']
            user.email = form.cleaned_data['email']
            user.phone_num = form.cleaned_data['phone_num']
            user.birth_date = form.cleaned_data['birth_date']
            user.gender = form.cleaned_data['gender']
            user.address = form.cleaned_data['address']
            user.district = form.cleaned_data['district']
            user.province = form.cleaned_data['province']
            user.postal_code = form.cleaned_data['postal_code']
            
            # บันทึกการเปลี่ยนแปลง
            user.save()
            
            messages.success(request, 'อัปเดตโปรไฟล์เรียบร้อยแล้ว')
            return redirect('user_profile:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'user_profile/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'user_profile/profile.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'อัปเดตโปรไฟล์เรียบร้อยแล้ว')
            return redirect('user_profile:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'user_profile/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            
            if not request.user.check_password(old_password):
                messages.error(request, 'รหัสผ่านเดิมไม่ถูกต้อง')
            elif new_password1 != new_password2:
                messages.error(request, 'รหัสผ่านใหม่ไม่ตรงกัน')
            else:
                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'เปลี่ยนรหัสผ่านเรียบร้อยแล้ว')
                return redirect('user_profile:profile')
    else:
        form = PasswordChangeForm()
    
    return render(request, 'user_profile/change_password.html', {'form': form})

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import User, Admin

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'user_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_name', 'address', 'district', 'province', 'postal_code', 'gender', 'birth_date', 'birth_month', 'birth_year', 'age', 'phone_num')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'user_name')
    ordering = ('email',)

class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'admin_name')

admin.site.register(User, CustomUserAdmin)
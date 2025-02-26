from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import *

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'user_name', 'is_staff', 'is_active', 'get_user_role')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_name', 'address', 'district', 'province', 'postal_code', 'gender', 'birth_date', 'phone_num')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'user_name')
    ordering = ('email',)

    def get_user_role(self, obj):
        return obj.user_role.user_role_name if obj.user_role else None
    get_user_role.short_description = 'User Role'

class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop', 'admin_role')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('user_role_id', 'user_role_name', 'description')
    search_fields = ('user_role_name',)

class AdminRoleAdmin(admin.ModelAdmin):
    list_display = ('admin_role_id', 'admin_role_name', 'description')
    search_fields = ('admin_role_name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'category', 'shop', 'price', 'quantity', 'created')
    search_fields = ('product_name', 'category__category_name', 'shop__shop_name')
    list_filter = ('category', 'shop')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'shop')
    search_fields = ('category_name', 'shop__shop_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Stock':
                return True
        return False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_price', 'order_date', 'status_order', 'place_delivery', 'shipper', 'tracking_num', 'delivery_date')
    search_fields = ('user__user_name', 'status_order__status_name', 'shipper__shipper_name')
    list_filter = ('status_order', 'shipper')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__order_id', 'product__product_name')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'payment_date', 'payment_status')
    search_fields = ('order__order_id', 'payment_status')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_id', 'order', 'payment', 'receipt_date')
    search_fields = ('order__order_id', 'payment__payment_id')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'order', 'product', 'rating','review_text','review_image', 'review_date') 
    search_fields = ('order__order_id', 'product__product_name', 'rating')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_id', 'order', 'reason', 'claim_status', 'claim_date')
    search_fields = ('order__order_id', 'reason', 'claim_status')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Sales staff':
                return True
        return False

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('promotion_id', 'promotion_name', 'discount', 'description', 'start_date', 'end_date')
    search_fields = ('promotion_name', 'description')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

class PromotionProductAdmin(admin.ModelAdmin):
    list_display = ('promotion_id', 'product_id')
    search_fields = ('promotion__promotion_name', 'product__product_name')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

class RecommendedProductAdmin(admin.ModelAdmin):
    list_display = ('recommended_product_id', 'user_id', 'product_id','recommended_date')
    search_fields = ('user__user_name', 'product__product_name')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('favorite_product_id', 'user_id', 'product_id','favorite_date')
    search_fields = ('user__user_name', 'product__product_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin:
                return qs.filter(shop=admin.shop)
        return qs.none()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            admin = Admin.objects.filter(user=request.user).first()
            if admin and admin.admin_role.admin_role_name == 'Board':
                return True
        return False

admin.site.register(User, CustomUserAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(UserRole, RoleAdmin)
admin.site.register(AdminRole, AdminRoleAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Claim, ClaimAdmin)
admin.site.register(Promotion, PromotionAdmin)
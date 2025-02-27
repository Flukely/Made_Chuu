from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import now
from main.models import *
from django.utils.html import format_html

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
    list_filter = ('admin_role',)
    search_fields = ('user__user_name',)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('user_role_id', 'user_role_name', 'description')
    search_fields = ('user_role_name',)

class AdminRoleAdmin(admin.ModelAdmin):
    list_display = ('admin_role_name', 'description')
    search_fields = ('admin_role_name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_image_thumbnail', 'product_name', 'category', 'quantity', 'price', 'shop', 'created')
    search_fields = ('product_name', 'category__category_name', 'quantity', 'price')
    list_filter = ('category',)
    
    def product_image_thumbnail(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="70" height="70" />', obj.product_image.url)
        return "No Image"
    product_image_thumbnail.short_description = 'Product Image'

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
    list_display = ('order_id', 'order_date', 'status_order', 'get_user_name', 'total_price', 'place_delivery', 'shipper', 'tracking_num', 'delivery_date')
    search_fields = ('user__user_name', 'status_order__status_name', 'shipper__shipper_name')
    list_filter = ('status_order', 'shipper')
    
    def get_user_name(self, obj):
        return obj.user.user_name
    get_user_name.short_description = 'User Name'
    
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
    list_display = ('payment_id', 'order', 'payment_status', 'payment_date', 'payment_proof_image')
    search_fields = ('order__order_id', 'payment_status', 'order__user__user_name')

    def payment_proof_image(self, obj):
        if obj.payment_image:
            return format_html('<img src="{}" width="250" height="350" />', obj.payment_image.url)
        return "No Image"
    payment_proof_image.short_description = 'Payment image'

    def save_model(self, request, obj, form, change):
        if change:  # ตรวจสอบว่าเป็นการแก้ไข record
            old_obj = Payment.objects.get(pk=obj.pk)
            if old_obj.payment_status != obj.payment_status:  # ตรวจสอบว่ามีการเปลี่ยนแปลงสถานะ
                if obj.payment_status == 'ตรวจสอบแล้ว':  # เงื่อนไขในการตรวจสอบค่า status
                    # เพิ่ม record ในตาราง Receipt
                    Receipt.objects.create(
                        order=obj.order,
                        payment=obj,
                        receipt_date=now()
                    )
        super().save_model(request, obj, form, change)
    
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
    list_display = ('receipt_id', 'receipt_date', 'order', 'payment')
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
    list_display = ('review_id', 'order', 'product', 'rating', 'review_date', 'review_text_admin', 'review_image_thumbnail')
    list_filter = ('rating',)
    search_fields = ('order__order_id', 'product__product_name', 'rating')
    
    def review_image_thumbnail(self, obj):
        if obj.review_image:
            return format_html('<img src="{}" width="150" height="200" />', obj.review_image.url)
        return "No Image"
    review_image_thumbnail.short_description = 'Review image'
    
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
    list_display = ('claim_id', 'claim_date', 'claim_status', 'order', 'promtpay_number', 'reason', 'comment', 'claim_image_thumbnail', 'claim_video')
    search_fields = ('order__order_id', 'reason', 'claim_status')
    
    def claim_image_thumbnail(self, obj):
        if obj.claim_image:
            return format_html('<img src="{}" width="150" height="200" />', obj.claim_image.url)
        return "No Image"
    claim_image_thumbnail.short_description = 'Claim image'
    
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
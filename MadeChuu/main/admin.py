from django.contrib import admin
from .models import StatusOrder, DeliveryStatus, Chat, ChatMessage, Admin, Cart, Category, Claim, Order, OrderProduct, Payment, Product, Receipt, Review, ShippingBrand, Shop, User

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'shop_id', 'admin_name', 'password')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'product_id', 'user_id', 'quantity', 'total_price')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'shop_id')

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_id', 'order_id', 'claim_date', 'claim_status', 'comment', 'claim_image', 'claim_video')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'quantity', 'total_price', 'shipper_id', 'order_date', 'delivery_date')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'quantity')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order_id', 'payment_date', 'payment_status', 'payment_image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'shop_id', 'product_name', 'description', 'price', 'quantity', 'category_id', 'product_image', 'created')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_id', 'payment_id', 'order_id', 'receipt_date')  # แก้ไขจาก Receipt_date เป็น receipt_date

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'order_id', 'product_id', 'review_date', 'rating', 'review_text', 'review_image')

@admin.register(ShippingBrand)
class ShippingBrandAdmin(admin.ModelAdmin):
    list_display = ('shipper_id', 'shipper_name', 'phone_num')

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_id', 'shop_name', 'owner_name', 'location', 'phone_num')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'address', 'district', 'province', 'postal_code', 'gender', 'age', 'email', 'phone_num', 'join_date', 'password')

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user_id')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'message', 'created')  # แก้ไขจาก ceated เป็น created

@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ('delivery_status_id', 'delivery_status_name')

@admin.register(StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    list_display = ('status_order_id', 'status_name')
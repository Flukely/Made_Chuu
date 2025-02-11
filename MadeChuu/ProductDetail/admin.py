from django.contrib import admin
from main.models import User, Product, Category, Shop, Cart, Order, OrderProduct, StatusOrder, ShippingBrand, Payment, Receipt, DeliveryStatus, Review, Claim, Chat, ChatMessage, Admin

@admin.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'email', 'phone_num', 'join_date')
    search_fields = ('user_name', 'email', 'phone_num')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'category', 'shop', 'price', 'quantity', 'created')
    search_fields = ('product_name', 'category__category_name', 'shop__shop_name')
    list_filter = ('category', 'shop')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'shop')
    search_fields = ('category_name', 'shop__shop_name')

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_id', 'shop_name', 'owner_name', 'phone_num')
    search_fields = ('shop_name', 'owner_name', 'phone_num')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user')
    search_fields = ('user__user_name', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_price', 'order_date', 'status_order', 'place_delivery', 'shipper', 'tracking_num', 'delivery_date')
    search_fields = ('user__user_name', 'status_order__status_name', 'shipper__shipper_name')
    list_filter = ('status_order', 'shipper')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__order_id', 'product__product_name')

@admin.register(StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    list_display = ('status_order_id', 'status_name')
    search_fields = ('status_name',)

@admin.register(ShippingBrand)
class ShippingBrandAdmin(admin.ModelAdmin):
    list_display = ('shipper_id', 'shipper_name', 'phone_num')
    search_fields = ('shipper_name', 'phone_num')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'payment_date', 'payment_status')
    search_fields = ('order__order_id', 'payment_status')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_id', 'order', 'payment', 'receipt_date')
    search_fields = ('order__order_id', 'payment__payment_id')

@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ('delivery_status_id', 'delivery_status_name')
    search_fields = ('delivery_status_name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'order', 'product', 'rating', 'review_date')
    search_fields = ('order__order_id', 'product__product_name', 'rating')

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_id', 'order', 'reason', 'claim_status', 'claim_date')
    search_fields = ('order__order_id', 'reason', 'claim_status')

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user')
    search_fields = ('user__user_name',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'message', 'created')
    search_fields = ('chat__chat_id', 'message')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'admin_name', 'shop')
    search_fields = ('admin_name', 'shop__shop_name')
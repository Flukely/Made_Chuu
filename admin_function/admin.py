from django.contrib import admin
from main.models import *

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_id', 'shop_name', 'owner_name', 'phone_num')
    search_fields = ('shop_name', 'owner_name', 'phone_num')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user')
    search_fields = ('user__user_name', )

@admin.register(StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    list_display = ('status_order_id', 'status_name')
    search_fields = ('status_name',)

@admin.register(ShippingBrand)
class ShippingBrandAdmin(admin.ModelAdmin):
    list_display = ('shipper_id', 'shipper_name', 'phone_num')
    search_fields = ('shipper_name', 'phone_num')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__cart_id', 'product__product_name')
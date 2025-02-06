from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'shop', 'product_name', 'description', 'price', 'quantity', 'category', 'product_image', 'created')
    list_filter = ("category")  # เพิ่ม Filter ให้เลือกหมวดหมู่และช่วงราคา

admin.site.register(Product)


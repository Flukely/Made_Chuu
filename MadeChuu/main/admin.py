from django.contrib import admin
from .models import Admin, Cart, Category, Claim, Delivery, FavoriteProducts, Order, OrderProducts, Payment, Product, Promotion, PromotionProducts, Receipt, RecommendedProduct, Review, ShippingBrand, Shop, Transaction, TransactionType, User  # นำเข้าโมเดลที่ต้องการลงทะเบียน

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'shop', 'firstname_admin', 'lastname_admin', 'password')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'product', 'user', 'quantity', 'total_price')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'shop')

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_id', 'order', 'claim_date', 'status', 'comment', 'claim_image', 'image_detail')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_id', 'order', 'shipper', 'delivery_date', 'delivery_status', 'tracking_num')

@admin.register(FavoriteProducts)
class FavoriteProductsAdmin(admin.ModelAdmin):
    list_display = ('favorite_products_id', 'product', 'user', 'added_date')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'place_delivery', 'total_price', 'shipper_id', 'order_date', 'delivery_date')

@admin.register(OrderProducts)
class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'payment_date', 'payment_status', 'image_payment')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'shop', 'product_name', 'description', 'price', 'quantity', 'category', 'product_image', 'created')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('promotion_id', 'promotion_name', 'promotion_type', 'discount', 'start_date', 'end_date', 'promotion_image')

@admin.register(PromotionProducts)
class PromotionProductsAdmin(admin.ModelAdmin):
    list_display = ('promotion', 'product')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_id', 'payment', 'order', 'receipt_date')

@admin.register(RecommendedProduct)
class RecommendedProductAdmin(admin.ModelAdmin):
    list_display = ('recommend_products_id', 'user', 'product', 'recommended_date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'order', 'review_date', 'rating', 'review_text')

@admin.register(ShippingBrand)
class ShippingBrandAdmin(admin.ModelAdmin):
    list_display = ('shipper_id', 'shipper_company', 'shipping_cost')

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_id', 'shop_name', 'owner_name', 'location', 'phone_num')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'transaction_type', 'transaction_date', 'admin')

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('transaction_type_id', 'transaction_name')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'address', 'district', 'province', 'post_code', 'gender', 'age', 'email', 'phone_num', 'join_date')
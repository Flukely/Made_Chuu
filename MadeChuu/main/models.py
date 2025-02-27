from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# Manager สำหรับสร้าง User และ Superuser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

# โมเดลผู้ใช้หลัก
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(null=True) # อนุญาตให้เป็นค่า null ได้
    phone_num = models.CharField(max_length=10)
    join_date = models.DateField(auto_now=True)
    user_role = models.ForeignKey('UserRole', on_delete=models.CASCADE, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']
    
    def __str__(self):
        return f"User: {self.email}"

# โมเดลสำหรับบทบาท
class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    user_role_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user_role_name

    class Meta:
        db_table = 'UserRole'

# โมเดลสำหรับบทบาทแอดมิน
class AdminRole(models.Model):
    admin_role_id = models.AutoField(primary_key=True)
    admin_role_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.admin_role_name

    class Meta:
        db_table = 'AdminRole'

# โมเดลสำหรับ Admin
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    admin_role = models.ForeignKey('AdminRole', on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin: {self.user.email}, Shop: {self.shop.shop_name}, Role: {self.admin_role.admin_role_name}"

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    product_image = models.ImageField(upload_to='product_image/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product ID: {self.product_id if self.product_id else 'No Product'}, Product Name: {self.product_name if self.product_name else 'No Product'}"
    class Meta:
        db_table = 'Product'

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name
    class Meta:
        db_table = 'Category'

class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=10)

    def __str__(self):
        return self.shop_name 
    class Meta:
        db_table = 'Shop'

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    total_price = models.FloatField()

    def __str__(self):
        return f"Cart ID: {self.cart_id if self.cart_id else 'No Cart'}, User ID: {self.user.user_id if self.user else 'No User'}"
    class Meta:
        db_table = 'Cart'

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Cart ID: {self.cart.cart_id if self.cart else 'No Cart'}, Product ID: {self.product.product_id if self.product else 'No Product'}"
    class Meta:
        db_table = 'CartItem'

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    total_price = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    status_order = models.ForeignKey('StatusOrder', on_delete=models.CASCADE, blank=True, null=True)
    place_delivery = models.CharField(max_length=255, blank=True, null=True)
    shipper = models.ForeignKey('ShippingBrand', on_delete=models.CASCADE, blank=True, null=True)
    tracking_num = models.CharField(max_length=255, blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    shop = models.ForeignKey('Shop' , on_delete=models.CASCADE ,blank= True , null=True)

    def __str__(self):
        return f"Order ID: {self.order_id if self.order_id else 'No Order'}, User ID: {self.user.user_id if self.user else 'No User'}"
    class Meta:
        db_table = 'Order'

class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order ID: {self.order.order_id if self.order else 'No Order'}, Product ID: {self.product.product_id if self.product else 'No Product'}"
    class Meta:
        db_table = 'OrderProduct'

class StatusOrder(models.Model):
    status_order_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255)

    def __str__(self):
        return self.status_name
    class Meta:
        db_table = 'StatusOrder'

class ShippingBrand(models.Model):
    shipper_id = models.AutoField(primary_key=True)
    shipper_name = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=10)

    def __str__(self):
        return f"Shipper ID: {self.shipper_id if self.shipper_id else 'No Shipper'}, Shipper Name: {self.shipper_name if self.shipper_name else 'No Shipper'}"
    class Meta:
        db_table = 'ShippingBrand'

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=255)
    payment_image = models.ImageField(upload_to='payment_image/', blank=True, null=True)

    def __str__(self):
        return f"Payment ID: {self.payment_id}, Order ID: {self.order.order_id if self.order else 'No Order'}, User ID: {self.order.user.user_id if self.order else 'No User'}"
    class Meta:
        db_table = 'Payment'

class Receipt(models.Model):
    receipt_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    receipt_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt ID: {self.receipt_id}, Order ID: {self.order.order_id if self.order else 'No Order'}, User ID: {self.order.user.user_id if self.order else 'No User'}"
    class Meta:
        db_table = 'Receipt'

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.CharField(max_length=255)
    review_image = models.ImageField(upload_to='review_image/', blank=True, null=True)
    review_text_admin = models.CharField(max_length=255, blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review ID: {self.review_id}, User ID: {self.order.user.user_id if self.order else 'No User'}, Product ID: {self.product.product_id if self.product else 'No Product'}"
    class Meta:
        db_table = 'Review'

class Claim(models.Model):
    claim_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    promtpay_number = models.CharField(max_length=255)
    claim_contact = models.CharField(max_length=255)
    claim_status = models.CharField(max_length=255)
    claim_video = models.FileField(upload_to='claim_video/', blank=True, null=True)
    claim_image = models.ImageField(upload_to='claim_image/', blank=True, null=True)
    claim_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim ID: {self.claim_id}, Order ID: {self.order.order_id if self.order else 'No Order'}, User ID: {self.order.user.user_id if self.order else 'No User'}"
    class Meta:
        db_table = 'Claim'

class Promotion(models.Model):
    promotion_id = models.AutoField(primary_key=True)
    promotion_name = models.CharField(max_length=255)
    promotion_type = models.CharField(max_length=255)
    discount = models.FloatField()
    description = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    promotion_image = models.ImageField(upload_to='promotion_image/', blank=True, null=True)

    def __str__(self):
        return f"Promotion ID: {self.promotion_id}, Promotion Name: {self.promotion_name}"

    class Meta:
        db_table = 'Promotion'

class PromotionProduct(models.Model):
    promotion_id = models.ForeignKey('Promotion', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"Promotion ID: {self.promotion_id.promotion_id if self.promotion_id else 'No Promotion'}, Product ID: {self.product_id.product_id if self.product_id else 'No Product'}"

    class Meta:
        db_table = 'PromotionProduct'

class RecommendedProduct(models.Model):
    recommended_product_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    recommended_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User ID: {self.user_id.user_id if self.user_id else 'No User'}, Product ID: {self.product_id.product_id if self.product_id else 'No Product'}"

    class Meta:
        db_table = 'RecommendedProduct'

class FavoriteProduct(models.Model):
    favorite_product_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    favorite_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User ID: {self.user_id.user_id if self.user_id else 'No User'}, Product ID: {self.product_id.product_id if self.product_id else 'No Product'}"

    class Meta:
        unique_together = (('product_id', 'user_id'),)
        db_table = 'FavoriteProduct'
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    email = models.EmailField()
    phone_num = models.CharField(max_length=10)
    join_date = models.DateField(auto_now=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"User ID: {self.user_id if self.user_id else 'No User'}, User Name: {self.user_name if self.user_name else 'No User'}"
    
    class Meta:
        db_table = 'user'

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    shop_id = models.ForeignKey('Shop', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    product_image = models.ImageField(upload_to='product_image/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product ID: {self.product_id if self.product_id else 'No Product'}, Product Name: {self.product_name if self.product_name else 'No Product'}"
    class Meta:
        db_table = 'product'

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    shop_id = models.ForeignKey('Shop', on_delete=models.CASCADE)

    def __str__(self):
        return f"Category ID: {self.category_id if self.category_id else 'No Category'}, Category Name: {self.category_name if self.category_name else 'No Category'}"
    class Meta:
        db_table = 'category'

class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=10)

    def __str__(self):
        return f"Shop ID: {self.shop_id if self.shop_id else 'No Shop'}, Shop Name: {self.shop_name if self.shop_name else 'No Shop'}"
    class Meta:
        db_table = 'shop'

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return f"Cart ID: {self.cart_id if self.cart_id else 'No Cart'}, User ID: {self.user_id if self.user_id else 'No User'}, Product ID: {self.product_id if self.product_id else 'No Product'}"
    class Meta:
        db_table = 'cart'

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    status_order_id = models.ForeignKey('StatusOrder', on_delete=models.CASCADE, blank=True, null=True)
    place_delivery = models.CharField(max_length=255, blank=True, null=True)
    shipper_id = models.ForeignKey('ShippingBrand', on_delete=models.CASCADE, blank=True, null=True)
    tracking_num = models.CharField(max_length=255, blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order ID: {self.order_id if self.order_id else 'No Order'}, User ID: {self.user_id if self.user_id else 'No User'}"
    class Meta:
        db_table = 'order'

class OrderProduct(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order ID: {self.order_id if self.order_id else 'No Order'}, Product ID: {self.product_id if self.product_id else 'No Product'}"
    class Meta:
        db_table = 'order_product'

class StatusOrder(models.Model):
    status_order_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Status Order ID: {self.status_order_id if self.status_order_id else 'No Status'}, Status Name: {self.status_name if self.status_name else 'No Status'}"
    class Meta:
        db_table = 'status_order'

class ShippingBrand(models.Model):
    shipper_id = models.AutoField(primary_key=True)
    shipper_name = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=10)

    def __str__(self):
        return f"Shipper ID: {self.shipper_id if self.shipper_id else 'No Shipper'}, Shipper Name: {self.shipper_name if self.shipper_name else 'No Shipper'}"
    class Meta:
        db_table = 'shipping_brand'

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=255)
    payment_image = models.ImageField(upload_to='payment_image/', blank=True, null=True)

    def __str__(self):
        return f"Payment ID: {self.payment_id}, Order ID: {self.order_id if self.order_id else 'No Order'}, User ID: {self.order_id.user_id if self.order_id else 'No User'}"
    class Meta:
        db_table = 'payment'

class Receipt(models.Model):
    receipt_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    payment_id = models.ForeignKey('Payment', on_delete=models.CASCADE)
    receipt_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt ID: {self.receipt_id}, Order ID: {self.order_id if self.order_id else 'No Order'}, User ID: {self.order_id.user_id if self.order_id else 'No User'}"
    class Meta:
        db_table = 'receipt'

class DeliveryStatus(models.Model):
    delivery_status_id = models.AutoField(primary_key=True)
    delivery_status_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Delivery ID: {self.delivery_status_id if self.delivery_status_id else 'No Delivery'}, Delivery Name: {self.delivery_status_name if self.delivery_status_name else 'No Delivery'}"
    class Meta:
        db_table = 'delivery_status'

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.CharField(max_length=255)
    review_image = models.ImageField(upload_to='review_image/', blank=True, null=True)
    review_text_admin = models.CharField(max_length=255, blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review ID: {self.review_id}, User ID: {self.order_id.user_id if self.order_id else 'No User'}, Product ID: {self.product_id if self.product_id else 'No Product'}"
    class Meta:
        db_table = 'review'

class Claim(models.Model):
    claim_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    promtpay_number = models.CharField(max_length=255)
    claim_contact = models.CharField(max_length=255)
    claim_status = models.CharField(max_length=255)
    claim_video = models.FileField(upload_to='claim_video/', blank=True, null=True)
    claim_image = models.ImageField(upload_to='claim_image/', blank=True, null=True)
    claim_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim ID: {self.claim_id}, Order ID: {self.order_id if self.order_id else 'No Order'}, User ID: {self.order_id.user_id if self.order_id else 'No User'}"
    class Meta:
        db_table = 'claim'

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat ID: {self.chat_id}, User ID: {self.user_id if self.user_id else 'No User'}"
    class Meta:
        db_table = 'chat'

class ChatMessage(models.Model):
    chat_id = models.ForeignKey('Chat', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat ID: {self.chat_id if self.chat_id else 'No Chat'}, Message: {self.message if self.message else 'No Message'}"
    class Meta:
        db_table = 'chat_message'

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=255)
    shop_id = models.ForeignKey('Shop', on_delete=models.CASCADE)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"Admin ID: {self.admin_id if self.admin_id else 'No Admin'}, Admin Name: {self.admin_name if self.admin_name else 'No Admin'}"
    class Meta:
        db_table = 'admin'
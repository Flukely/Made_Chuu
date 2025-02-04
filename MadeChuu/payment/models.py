# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User
from django.db import models


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)
    firstname_admin = models.CharField(max_length=100, blank=True, null=True)
    lastname_admin = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Claim(models.Model):
    claim_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', models.DO_NOTHING, blank=True, null=True)
    claim_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    claim_image = models.CharField(max_length=255, blank=True, null=True)
    image_detail = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'claim'


class Delivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', models.DO_NOTHING, blank=True, null=True)
    shipper = models.ForeignKey('ShippingBrand', models.DO_NOTHING, blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    delivery_status = models.CharField(max_length=50, blank=True, null=True)
    tracking_num = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delivery'


class FavoriteProducts(models.Model):
    favorite_products_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    added_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favorite_products'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    place_delivery = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipper_id = models.IntegerField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        # คืนค่าเลข order_id และชื่อผู้ใช้
        return f"Order ID: {self.order_id}, User: {self.user.user_name if self.user else 'No User'}"

    class Meta:
        managed = False
        db_table = 'order'


class OrderProducts(models.Model):
    order = models.OneToOneField(Order, models.DO_NOTHING, primary_key=True)  # The composite primary key (order_id, product_id) found, that is not supported. The first column is selected.
    product = models.ForeignKey('Product', models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_products'
        unique_together = (('order', 'product'),)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', models.DO_NOTHING, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    image_payment = models.ImageField(upload_to='receipts/', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    product_image = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Promotion(models.Model):
    promotion_id = models.AutoField(primary_key=True)
    promotion_name = models.CharField(max_length=255, blank=True, null=True)
    promotion_type = models.CharField(max_length=50, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    promotion_image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'promotion'


class PromotionProducts(models.Model):
    promotion = models.OneToOneField(Promotion, models.DO_NOTHING, primary_key=True)  # The composite primary key (promotion_id, product_id) found, that is not supported. The first column is selected.
    product = models.ForeignKey(Product, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'promotion_products'
        unique_together = (('promotion', 'product'),)


class Receipt(models.Model):
    receipt_id = models.AutoField(primary_key=True)
    payment = models.ForeignKey(Payment, models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey(Order, models.DO_NOTHING, blank=True, null=True)
    receipt_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receipt'


class RecommendedProduct(models.Model):
    recommend_products_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    recommended_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recommended_product'


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING, blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    review_text = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'


class ShippingBrand(models.Model):
    shipper_id = models.AutoField(primary_key=True)
    shipper_company = models.CharField(max_length=255, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shipping_brand'


class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_num = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop'


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING, blank=True, null=True)
    transaction_type = models.ForeignKey('TransactionType', models.DO_NOTHING, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    admin = models.ForeignKey(Admin, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction'


class TransactionType(models.Model):
    transaction_type_id = models.AutoField(primary_key=True)
    transaction_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction_type'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    post_code = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_num = models.CharField(max_length=15, blank=True, null=True)
    join_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

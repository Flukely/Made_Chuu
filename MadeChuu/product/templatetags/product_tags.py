from django import template
from main.models import PromotionProduct

register = template.Library()

@register.filter(name='get_discounted_price')
def get_discounted_price(product):
    """คำนวณราคาหลังลด (ถ้ามีโปรโมชัน)"""
    try:
        promo = PromotionProduct.objects.filter(product_id=product).first()
        if promo:
            discount = promo.promotion_id.discount
            return product.price * (1 - discount / 100)
        return product.price
    except:
        return product.price

@register.filter(name='is_on_promotion')
def is_on_promotion(product):
    """ตรวจสอบว่าสินค้าอยู่ในโปรโมชันหรือไม่"""
    return PromotionProduct.objects.filter(product_id=product).exists()
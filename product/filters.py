import django_filters
from main.models import Product, Category, Shop

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Category',
        empty_label='All',
    )

    class Meta:
        model = Product
        fields = ['category']

class ShopFilter(django_filters.FilterSet):
    shop = django_filters.ModelChoiceFilter(
        field_name='shop_name',  # ตรวจสอบให้แน่ใจว่าใช้ field_name แทน feild_name
        queryset=Shop.objects.all(),
        label='Shop',
        empty_label='All',
    )

    class Meta:
        model = Product
        fields = ['shop']
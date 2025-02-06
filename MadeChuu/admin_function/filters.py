import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), 
        label="Category",
        empty_label="Select Category",
    )
        
    class Meta:
        model = Product
        fields = ["category"]
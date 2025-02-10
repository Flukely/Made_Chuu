import django_filters
from main.models import *

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), 
        label="Category",
        empty_label="ทั้งหมด",
    )
        
    class Meta:
        model = Product
        fields = ["category"]

class OrderFilter(django_filters.FilterSet):
    status_order = django_filters.ModelChoiceFilter(
        queryset=StatusOrder.objects.all(), 
        label="Status Order",
        empty_label="ทั้งหมด",
    )
    class Meta:
        model = Order
        fields = ["status_order"]

    # class DeliveryFilter(django_filters.FilterSet):
    #     delivery_status = django_filters.ChoiceFilter(
    #         choices=[
    #             ('preparing', 'Preparing'),
    #             ('sending', 'Sending'),
    #             ('transition', 'Transition'),
    #             ('successfully', 'Successfully'),
    #         ],
    #         label="Delivery Status",
    #         empty_label="ทั้งหมด",
    #     )
    #     class Meta:
    #         model = Delivery
    #         fields = ["delivery_status"]
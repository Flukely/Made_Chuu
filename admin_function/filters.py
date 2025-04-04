import django_filters
from main.models import *
from .models import *

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
    status_order = django_filters.ChoiceFilter(
        choices = [
            (2, "จ่ายเงินแล้ว"),  
            (3, "กำลังแพ็คของ"),  
            (4, "เตรียมส่ง"),  
            (5, "กำลังจัดส่ง"),  
            (6, "ส่งสำเร็จ"),  
            (7, "เคลมสินค้า"), 
        ],
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
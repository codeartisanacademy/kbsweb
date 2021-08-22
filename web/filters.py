import django_filters
from .models import Invoice

class InvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Invoice
        fields = ['delivery_order__customer', 'delivery_order__sales', 'delivery_order__category']

    
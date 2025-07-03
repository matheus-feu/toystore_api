from django.contrib import admin

from toy_store.models import Customer
from toy_store.models import Sale


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'date_of_birth', 'created_at', 'updated_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at', 'updated_at')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'sale_date', 'total_amount')
    search_fields = ('customer__name', 'customer__email')
    list_filter = ('sale_date',)

    def total_amount(self, obj):
        return f"${obj.total_amount:.2f}"

    total_amount.short_description = 'Total Amount'
    total_amount.admin_order_field = 'total_amount'
    total_amount.empty_value_display = 'N/A'

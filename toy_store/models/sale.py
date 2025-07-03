from django.db import models

from core.models import BaseModel
from toy_store.models.customer import Customer


class Sale(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    sale_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Sale {self.id} - {self.customer.name} on {self.sale_date.strftime("%Y-%m-%d %H:%M:%S")}'

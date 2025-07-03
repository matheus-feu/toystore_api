from django.urls import path

from toy_store.views import CustomerCreateView, SalesFormView

app_name = 'toy_store'

urlpatterns = [
    path('clientes/', CustomerCreateView.as_view(), name='customer_view'),
    path('vendas/nova/', SalesFormView.as_view(), name='sales_view'),
]

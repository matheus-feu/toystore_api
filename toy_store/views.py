from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomerForm, SaleForm
from .models import Customer, Sale


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'toy_store/customer_form.html'
    success_url = reverse_lazy('toy_store:customer_view')



class SalesFormView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'toy_store/sales_form.html'
    success_url = reverse_lazy('toy_store:sales_view')
from django import forms

from toy_store.models import Customer, Sale


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'email',
            'date_of_birth',
            'phone',
            'address',
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Nome completo",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email",
                    "class": "form-control",
                }
            ),
            "date_of_birth": forms.DateInput(
                attrs={
                    "placeholder": "Data de nascimento (YYYY-MM-DD)",
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Telefone (apenas números)",
                    "class": "form-control",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Endereço completo",
                    "class": "form-control",
                }
            ),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            'customer',
            'total_amount',
        ]
        widgets = {
            "customer": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "total_amount": forms.NumberInput(
                attrs={
                    "placeholder": "Valor total",
                    "class": "form-control",
                }
            ),
        }

from datetime import date

from django.core.validators import RegexValidator
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from toy_store.models.customer import Customer


class CustomerDetailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    date_of_birth = serializers.DateField()
    phone = serializers.CharField(
        validators=[RegexValidator(r'^\d{8,15}$', message='Telefone inválido')]
    )
    address = serializers.CharField()


class CustomerInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    details = CustomerDetailSerializer(source='*')


class SaleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    sale_date = serializers.SerializerMethodField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    @extend_schema_field(serializers.CharField())
    def get_sale_date(self, obj):
        value = obj.sale_date
        if hasattr(value, 'date'):
            return value.date().isoformat()
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        return str(value)

    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor total deve ser maior que zero.")
        return value


class CustomerListSerializer(serializers.Serializer):
    info = CustomerInfoSerializer(source='*')
    stats = serializers.SerializerMethodField()

    @extend_schema_field(serializers.DictField())
    def get_stats(self, obj):
        return {}


class CustomerSerializer(serializers.ModelSerializer):
    info = CustomerInfoSerializer(source='*')
    stats = serializers.SerializerMethodField()
    duplicates = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'info', 'stats', 'duplicates', 'created_at', 'updated_at']

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError("A data de nascimento não pode ser futura.")
        return value

    @extend_schema_field(serializers.DictField())
    def get_stats(self, obj):
        return {'sales': SaleSerializer(obj.sales.all(), many=True).data}

    @extend_schema_field(serializers.ListField(child=CustomerListSerializer()))
    def get_duplicates(self, obj):
        duplicates = Customer.objects.filter(
            name=obj.name,
            email=obj.email
        ).exclude(id=obj.id)
        return CustomerListSerializer(duplicates, many=True).data


class SalesPerDaySerializer(serializers.Serializer):
    sale_date = serializers.SerializerMethodField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)

    @extend_schema_field(serializers.CharField())
    def get_sale_date(self, obj):
        value = obj['sale_date']
        if hasattr(value, 'date'):
            return value.date().isoformat()
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        return str(value)


class CustomerHighlightSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(allow_null=True)
    customer_name = serializers.CharField(allow_null=True)
    value = serializers.CharField(allow_null=True)
